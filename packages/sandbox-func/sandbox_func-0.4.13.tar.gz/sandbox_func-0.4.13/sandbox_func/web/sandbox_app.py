import logging
import os

from fastapi import FastAPI
from fastapi import Request, Body
from fastapi.middleware.cors import CORSMiddleware

from sandbox_func.common.request.CybotronClient import TENANT_ID
from sandbox_func.common.lang.async_requests import AsyncRequests
from sandbox_func.common.log.AwLogger import AwLogger, Log, LogRecord
from sandbox_func.common.lang import logger_setting
from sandbox_func.request.SFRequest import SFRequest
from sandbox_func.request.SFResponse import SFResponse
from sandbox_func.service.SandboxFuncService import SandboxFuncService
from sandbox_func.service.SandboxCallbackService import SandboxCallbackService

logger_setting.init()
aw_logger = AwLogger.getLogger(__name__)
logger = logging.getLogger(__name__ + "_logger")

app = FastAPI(title="Autowork Sandbox Function")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    if os.getenv('BUSINESS_KEY'):
        # 通知边车启动成功
        client = AsyncRequests(base_url='http://localhost:9000')
        request = client.build_request(method='get', url=f"/business/call/{os.getenv('BUSINESS_KEY')}")
        await client.send(request=request)


@app.get("/health")
async def health():
    return {
        "pid": os.getpid()
    }


@app.post("/sandbox/call")
async def call_sandbox_func(body=Body(...)):
    """ 线上同步接口 """
    response = SFResponse()
    token = None
    try:
        logger.info(f'收到沙盒函数请求，请求参数：{body}')
        token = TENANT_ID.set(body['tenant_id'])
        request = SFRequest(class_file=body['class_file'], method_name=body['method_name'],
                            request_id=body['request_id'], input=body['input'])
        # log_record = AwLogger.init_logger(body['trace_id'], {"app_id": body['app_id'], "func_id": body['func_id']})
        # aw_logger.info('沙盒函数调试模式运行，请求信息：{}'.format(request), log_record)
        response = await SandboxFuncService.call(request)

        if response.error:
            response.success = False
        else:
            response.success = True
        return response
    except BaseException as e:
        # if log_record is not None:
        #     aw_logger.error('沙盒函数调试模式运行失败, 错误信息：{}'.format(e), log_record)
        logger.exception(e)
        response.success = False
        response.error = str(e)
        return response
    finally:
        if token is not None:
            TENANT_ID.reset(token)


@app.post("/sandbox/call/async")
async def call_sandbox_func_async(body=Body(...)):
    """线上异步接口"""
    response = SFResponse()
    token = None
    try:
        logger.info(f'收到沙盒函数请求，请求参数：{body}')
        token = TENANT_ID.set(body['tenant_id'])
        request = SFRequest(class_file=body['class_file'], method_name=body['method_name'], job_id=body['job_id'],
                            input=body['input'], request_id=body['request_id'], hook=body['hook'])
        # await service.create_async_job(request.app_id, request.request_id, status="PROCESSING", progress=1)
        response = await SandboxFuncService.call(request)  # 重新生成response
        await SandboxCallbackService.callback(request, response)        # 如果是异步执行，且请求参数指定了hook，则进行回调
        response.error = response.job.job_error if response.job.job_error else response.error  # 若job有错误，则覆盖response的错误
        if response.error:
            response.success = False
            await SandboxFuncService.update_async_job(request.job_id, status="FAILED", progress=100,
                                                      error_message=response.error)
        else:
            response.success = True
            await SandboxFuncService.update_async_job(request.job_id, status="SUCCESS", progress=100)
        return response
    except BaseException as e:
        logger.exception(f'处理沙盒函数调用报错，报错信息：{e}')
        response.success = False
        response.error = str(e)
        return response
    finally:
        if token is not None:
            TENANT_ID.reset(token)
