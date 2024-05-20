from typing import Any

from afeng_tools.fastapi_tool.common.po_service.base_po_service import PoService
from afeng_tools.pydantic_tool.model.common_models import LinkItem


class TagPoService(PoService):
    """
    使用示例：tag_po_service = TagPoService(app_info.db_code, TagInfoPo)
    """
    _table_name_ = "tb_tag_info"

    def get_by_code(self, type_code: str, code: str) -> Any:
        return self.get(self.model_type.type_code == type_code, self.model_type.code == code)

    @classmethod
    def convert_to_link_item(cls, tag_po, is_active: bool = False, tag_href_prefix: str = '/tag') -> LinkItem:
        return LinkItem(
            title=tag_po.title,
            href=f'{tag_href_prefix}/{tag_po.code}',
            code=tag_po.code,
            description=tag_po.description,
            is_active=is_active)


class TagRelationPoService(PoService):
    """
    使用示例：tag_relation_po_service = TagRelationPoService(app_info.db_code, TagRelationInfoPo)
    """
    _table_name_ = "tb_tag_relation_info"

    def query_by_type_code(self, type_code: str) -> list[Any]:
        return self.get(self.model_type.type_code == type_code)

    def get_by_tag_code(self, type_code: str, tag_code: str) -> Any:
        return self.get(self.model_type.type_code == type_code, self.model_type.tag_code == tag_code)

