import uuid
import base62
import time
from datetime import datetime


def format_time_ago(unix_timestamp) -> str:
    """
    Convert a Unix timestamp to a user-friendly time string.
    """
    try:
        unix_timestamp = int(unix_timestamp)
    except:
        return unix_timestamp

    now = int(time.time())
    unix_timestamp = int(unix_timestamp)
    diff = now - unix_timestamp

    # Time calculations
    minute = 60
    hour = 60 * minute
    day = 24 * hour

    if diff < hour:
        return f"{diff // minute} minutes ago" if diff >= minute else "Just now"
    elif diff < day:
        hours = diff // hour
        minutes = (diff % hour) // minute
        return f"{hours} hours {minutes} minutes ago" if minutes else f"{hours} hours ago"
    elif diff < 3 * day:
        return f"{diff // day} days ago"
    else:
        # Convert to specific date and time format for durations longer than 3 days
        return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


def dict_to_markdown(d, indent=0, table_format_keys=()):
    # table_format_keys 中的key，会用table来展示，否则默认用列表展示
    # 假定table_format_keys 中的key对应的value是list，且list中的元素是dict，且dict的key是一样的
    markdown = ""
    if isinstance(d, dict):
        for key, value in d.items():
            # print(f"key: {key}, value: {value}, type: {type(value)}")
            if key in table_format_keys and value:
                # 特殊处理fields为表格，动态获取列名
                headers = value[0].keys()  # 从第一个元素获取所有键作为表头
                markdown += f"{'  ' * indent}* **{key}**: \n\n"
                markdown += f"{'  ' * indent}" + " | ".join(headers) + "\n"
                markdown += f"{'  ' * indent}" + " | ".join(["---"]*len(headers)) + "\n"
                for field in value:
                    markdown += f"{'  ' * indent}" + " | ".join([str(field[h]) for h in headers]) + "\n"
            else:
                markdown += f"{'  ' * indent}* **{key}**: "
                if isinstance(value, (dict, list)):
                    markdown += "\n" + dict_to_markdown(value, indent+1, table_format_keys=table_format_keys)
                else:
                    markdown += f"{value}\n"
    elif isinstance(d, list):
        for item in d:
            if isinstance(item, (dict, list)):
                markdown += dict_to_markdown(item, indent, table_format_keys=table_format_keys)
            else:
                markdown += f"{'  ' * indent}* {item}\n"
    return markdown


def gen_base62_uuid():
    # 生成一个 UUID
    my_uuid = uuid.uuid4()
    # 转换 UUID 的整数表示为 Base62
    base62_uuid = base62.encode(int(my_uuid))
    return base62_uuid


def gen_id(prefix=None):
    if prefix:
        return f"{prefix}_{gen_base62_uuid()}"
    else:
        return gen_base62_uuid()


def gen_tenant_id():
    return f"t_{gen_base62_uuid()}"

def gen_token_id():
    return f"token_{gen_base62_uuid()}"


def gen_datasource_id():
    return f"ds_{gen_base62_uuid()}"


def gen_id_for_chat():
    return f"chat_{gen_base62_uuid()}"


def gen_id_for_msg():
    return f"msg_{gen_base62_uuid()}"


def gen_id_for_run():
    return f"run_{gen_base62_uuid()}"

def ctime_chn():
    # 获取当前时间
    now = datetime.now()
    # 注意：中文日期时间格式可以根据需要进行调整
    chinese_weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    # 获取星期几的数字（0-6），然后将其转换为中文名称
    weekday_cn = chinese_weekday[now.weekday()]
    date_time = now.strftime("%Y年%m月%d日%H时%M分%S秒")
    chinese_time_full_format = f"{date_time}{weekday_cn}"
    return chinese_time_full_format


