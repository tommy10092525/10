import datetime

def generate_caption(time:str):
    now=datetime.datetime.now()
    created_at=datetime.datetime.strptime(time[:-8],"%Y-%m-%d %X")
    diff=now-created_at
    if diff.seconds<60:
        return "たった今"
    elif diff.seconds<3600:
        return f"{diff.seconds//60}分前"
    elif diff.days<1:
        return f"{diff.seconds//3600}時間前"
    elif diff.days<30:
        return f"{diff.days}日前"
    elif diff.days<365:
        return f"{diff.days//30.5}ヶ月前"
    else:
        return f"{diff.days//365}年前"

if __name__=="__main__":
    print(generate_caption(datetime.datetime(2024,10,1,0,0,0)))
    