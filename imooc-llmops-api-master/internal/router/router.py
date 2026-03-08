#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 15:01
@Author  : thezehui@gmail.com
@File    : router.py
"""
from dataclasses import dataclass
from uuid import UUID

from fastapi import FastAPI, Depends
from injector import inject

from internal.handler import (
    AppHandler,
    BuiltinToolHandler,
    ApiToolHandler,
    UploadFileHandler,
    DatasetHandler,
    DocumentHandler,
    SegmentHandler,
    OAuthHandler,
    AccountHandler,
    AuthHandler,
    AIHandler,
    ApiKeyHandler,
    OpenAPIHandler,
    BuiltinAppHandler,
    WorkflowHandler,
    LanguageModelHandler,
    AssistantAgentHandler,
    AnalysisHandler,
    WebAppHandler,
    ConversationHandler,
)
from internal.dependencies import get_current_user, get_api_key_user


@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler
    builtin_tool_handler: BuiltinToolHandler
    api_tool_handler: ApiToolHandler
    upload_file_handler: UploadFileHandler
    dataset_handler: DatasetHandler
    document_handler: DocumentHandler
    segment_handler: SegmentHandler
    oauth_handler: OAuthHandler
    account_handler: AccountHandler
    auth_handler: AuthHandler
    ai_handler: AIHandler
    api_key_handler: ApiKeyHandler
    openapi_handler: OpenAPIHandler
    builtin_app_handler: BuiltinAppHandler
    workflow_handler: WorkflowHandler
    language_model_handler: LanguageModelHandler
    assistant_agent_handler: AssistantAgentHandler
    analysis_handler: AnalysisHandler
    web_app_handler: WebAppHandler
    conversation_handler: ConversationHandler

    def register_router(self, app: FastAPI):
        """注册路由"""

        # 1. 应用模块路由
        app.get("/ping")(self.app_handler.ping)
        app.get("/apps")(self.app_handler.get_apps_with_page)
        app.post("/apps")(self.app_handler.create_app)
        app.get("/apps/{app_id}")(self.app_handler.get_app)
        app.post("/apps/{app_id}")(self.app_handler.update_app)
        app.post("/apps/{app_id}/delete")(self.app_handler.delete_app)
        app.post("/apps/{app_id}/copy")(self.app_handler.copy_app)
        app.get("/apps/{app_id}/draft-app-config")(self.app_handler.get_draft_app_config)
        app.post("/apps/{app_id}/draft-app-config")(self.app_handler.update_draft_app_config)
        app.post("/apps/{app_id}/publish")(self.app_handler.publish)
        app.post("/apps/{app_id}/cancel-publish")(self.app_handler.cancel_publish)
        app.get("/apps/{app_id}/publish-histories")(self.app_handler.get_publish_histories_with_page)
        app.post("/apps/{app_id}/fallback-history")(self.app_handler.fallback_history_to_draft)
        app.get("/apps/{app_id}/summary")(self.app_handler.get_debug_conversation_summary)
        app.post("/apps/{app_id}/summary")(self.app_handler.update_debug_conversation_summary)
        app.post("/apps/{app_id}/conversations/delete-debug-conversation")(self.app_handler.delete_debug_conversation)
        app.post("/apps/{app_id}/conversations")(self.app_handler.debug_chat)
        app.post("/apps/{app_id}/conversations/tasks/{task_id}/stop")(self.app_handler.stop_debug_chat)
        app.get("/apps/{app_id}/conversations/messages")(self.app_handler.get_debug_conversation_messages_with_page)
        app.get("/apps/{app_id}/published-config")(self.app_handler.get_published_config)
        app.post("/apps/{app_id}/published-config/regenerate-web-app-token")(self.app_handler.regenerate_web_app_token)

        # 2. 内置插件广场模块
        app.get("/builtin-tools")(self.builtin_tool_handler.get_builtin_tools)
        app.get("/builtin-tools/{provider_name}/tools/{tool_name}")(self.builtin_tool_handler.get_provider_tool)
        app.get("/builtin-tools/{provider_name}/icon")(self.builtin_tool_handler.get_provider_icon)
        app.get("/builtin-tools/categories")(self.builtin_tool_handler.get_categories)

        # 3. 自定义API插件模块
        app.get("/api-tools")(self.api_tool_handler.get_api_tool_providers_with_page)
        app.post("/api-tools/validate-openapi-schema")(self.api_tool_handler.validate_openapi_schema)
        app.post("/api-tools")(self.api_tool_handler.create_api_tool_provider)
        app.get("/api-tools/{provider_id}")(self.api_tool_handler.get_api_tool_provider)
        app.post("/api-tools/{provider_id}")(self.api_tool_handler.update_api_tool_provider)
        app.get("/api-tools/{provider_id}/tools/{tool_name}")(self.api_tool_handler.get_api_tool)
        app.post("/api-tools/{provider_id}/delete")(self.api_tool_handler.delete_api_tool_provider)

        # 4. 上传文件模块
        app.post("/upload-files/file")(self.upload_file_handler.upload_file)
        app.post("/upload-files/image")(self.upload_file_handler.upload_image)

        # 5. 知识库模块
        app.get("/datasets")(self.dataset_handler.get_datasets_with_page)
        app.post("/datasets")(self.dataset_handler.create_dataset)
        app.get("/datasets/{dataset_id}")(self.dataset_handler.get_dataset)
        app.post("/datasets/{dataset_id}")(self.dataset_handler.update_dataset)
        app.get("/datasets/{dataset_id}/queries")(self.dataset_handler.get_dataset_queries)
        app.post("/datasets/{dataset_id}/delete")(self.dataset_handler.delete_dataset)
        app.get("/datasets/{dataset_id}/documents")(self.document_handler.get_documents_with_page)
        app.post("/datasets/{dataset_id}/documents")(self.document_handler.create_documents)
        app.get("/datasets/{dataset_id}/documents/{document_id}")(self.document_handler.get_document)
        app.post("/datasets/{dataset_id}/documents/{document_id}/name")(self.document_handler.update_document_name)
        app.post("/datasets/{dataset_id}/documents/{document_id}/enabled")(self.document_handler.update_document_enabled)
        app.post("/datasets/{dataset_id}/documents/{document_id}/delete")(self.document_handler.delete_document)
        app.get("/datasets/{dataset_id}/documents/batch/{batch}")(self.document_handler.get_documents_status)
        app.get("/datasets/{dataset_id}/documents/{document_id}/segments")(self.segment_handler.get_segments_with_page)
        app.post("/datasets/{dataset_id}/documents/{document_id}/segments")(self.segment_handler.create_segment)
        app.get("/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}")(self.segment_handler.get_segment)
        app.post("/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}")(self.segment_handler.update_segment)
        app.post("/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/enabled")(self.segment_handler.update_segment_enabled)
        app.post("/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/delete")(self.segment_handler.delete_segment)
        app.post("/datasets/{dataset_id}/hit")(self.dataset_handler.hit)

        # 6. 授权认证模块
        app.get("/oauth/{provider_name}")(self.oauth_handler.provider)
        app.post("/oauth/authorize/{provider_name}")(self.oauth_handler.authorize)
        app.post("/auth/password-login")(self.auth_handler.password_login)
        app.post("/auth/logout")(self.auth_handler.logout)

        # 7. 账号设置模块
        app.get("/account")(self.account_handler.get_current_user)
        app.post("/account/password")(self.account_handler.update_password)
        app.post("/account/name")(self.account_handler.update_name)
        app.post("/account/avatar")(self.account_handler.update_avatar)

        # 8. AI辅助模块
        app.post("/ai/optimize-prompt")(self.ai_handler.optimize_prompt)
        app.post("/ai/suggested-questions")(self.ai_handler.generate_suggested_questions)

        # 9. API秘钥模块
        app.get("/openapi/api-keys")(self.api_key_handler.get_api_keys_with_page)
        app.post("/openapi/api-keys")(self.api_key_handler.create_api_key)
        app.post("/openapi/api-keys/{api_key_id}")(self.api_key_handler.update_api_key)
        app.post("/openapi/api-keys/{api_key_id}/is-active")(self.api_key_handler.update_api_key_is_active)
        app.post("/openapi/api-keys/{api_key_id}/delete")(self.api_key_handler.delete_api_key)
        app.post("/openapi/chat")(self.openapi_handler.chat)

        # 10. 内置应用模块
        app.get("/builtin-apps/categories")(self.builtin_app_handler.get_builtin_app_categories)
        app.get("/builtin-apps")(self.builtin_app_handler.get_builtin_apps)
        app.post("/builtin-apps/add-builtin-app-to-space")(self.builtin_app_handler.add_builtin_app_to_space)

        # 11. 工作流模块
        app.get("/workflows")(self.workflow_handler.get_workflows_with_page)
        app.post("/workflows")(self.workflow_handler.create_workflow)
        app.get("/workflows/{workflow_id}")(self.workflow_handler.get_workflow)
        app.post("/workflows/{workflow_id}")(self.workflow_handler.update_workflow)
        app.post("/workflows/{workflow_id}/delete")(self.workflow_handler.delete_workflow)
        app.post("/workflows/{workflow_id}/draft-graph")(self.workflow_handler.update_draft_graph)
        app.get("/workflows/{workflow_id}/draft-graph")(self.workflow_handler.get_draft_graph)
        app.post("/workflows/{workflow_id}/debug")(self.workflow_handler.debug_workflow)
        app.post("/workflows/{workflow_id}/publish")(self.workflow_handler.publish_workflow)
        app.post("/workflows/{workflow_id}/cancel-publish")(self.workflow_handler.cancel_publish_workflow)

        # 12. 语言模型模块
        app.get("/language-models")(self.language_model_handler.get_language_models)
        app.get("/language-models/{provider_name}/icon")(self.language_model_handler.get_language_model_icon)
        app.get("/language-models/{provider_name}/{model_name}")(self.language_model_handler.get_language_model)

        # 13. 辅助Agent模块
        app.post("/assistant-agent/chat")(self.assistant_agent_handler.assistant_agent_chat)
        app.post("/assistant-agent/chat/{task_id}/stop")(self.assistant_agent_handler.stop_assistant_agent_chat)
        app.get("/assistant-agent/messages")(self.assistant_agent_handler.get_assistant_agent_messages_with_page)
        app.post("/assistant-agent/delete-conversation")(self.assistant_agent_handler.delete_assistant_agent_conversation)

        # 14. 应用统计模块
        app.get("/analysis/{app_id}")(self.analysis_handler.get_app_analysis)

        # 15. WebApp模块
        app.get("/web-apps/{token}")(self.web_app_handler.get_web_app)
        app.post("/web-apps/{token}/chat")(self.web_app_handler.web_app_chat)
        app.post("/web-apps/{token}/chat/{task_id}/stop")(self.web_app_handler.stop_web_app_chat)
        app.get("/web-apps/{token}/conversations")(self.web_app_handler.get_conversations)

        # 16. 会话模块
        app.get("/conversations/{conversation_id}/messages")(self.conversation_handler.get_conversation_messages_with_page)
        app.post("/conversations/{conversation_id}/delete")(self.conversation_handler.delete_conversation)
        app.post("/conversations/{conversation_id}/messages/{message_id}/delete")(self.conversation_handler.delete_message)
        app.get("/conversations/{conversation_id}/name")(self.conversation_handler.get_conversation_name)
        app.post("/conversations/{conversation_id}/name")(self.conversation_handler.update_conversation_name)
        app.post("/conversations/{conversation_id}/is-pinned")(self.conversation_handler.update_conversation_is_pinned)
