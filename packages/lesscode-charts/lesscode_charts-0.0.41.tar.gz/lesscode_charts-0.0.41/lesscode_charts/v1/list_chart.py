from typing import Union


class ListChart:
    @staticmethod
    def list_chart(columns: Union[list, dict], data: list, total: int = 0, count: int = 0, page_num=1, page_size=10,
                   index_enable=False, index_name="序号", index_key="index", title="") -> dict:
        """

        :param title:
        :param index_key:
        :param index_name:
        :param index_enable:
        :param page_size:
        :param page_num:
        :param count:
        :param total: 总数
        :param columns: [{"title":"","dataIndex":""}] or {"名称":"字段名"}
        :param data:
        :return:
        """
        if isinstance(columns, dict):
            columns = [{"title": k, "dataIndex": v} for k, v in columns.items()]
        if index_enable:
            columns = [{"title": index_name, "dataIndex": index_key}] + columns
            data = [{**_, index_key: (page_num - 1) * page_size + i} for i, _ in enumerate(data)]
        return {
            "chart_type": "list",
            "title": title,
            "columns": columns,
            "data": data,
            "total": total,
            "count": count
        }
