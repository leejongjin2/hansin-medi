import schedule
import datetime
from hwiUtils.SchedulerDatabase import update_hanshinInferenceTB, update_hanshinTrainTB, update_infinityTrainTB, update_outlierTB
from hwiUtils.train import train_HanshinModel, train_InfinityModel
from hwiUtils.inference import inference

def updateDatabase():
    # Update HanshinTrainTB, InfinityTrainTB Quarterly and Train New Models
    # 분기업데이트 되었는지 확인 추가
    # and day = 1일
    if (datetime.datetime.now().month % 3 == 1 ):
        update_hanshinTrainTB()
        update_infinityTrainTB()
        
        update_outlierTB()        
        
        train_HanshinModel()
        train_InfinityModel()
    
    # Update Hanshin Inference data Everyday and Inference with updated data
    update_hanshinInferenceTB()
    inference()        

if __name__ == "__main__":
    # HH:MM:SS에 작업 실행 -> 매 00시 1분에 실행
    # schedule.every().day.at("14:45:50").do(updateDatabase)
    schedule.every(5).seconds.do(updateDatabase)
    while 1:
        schedule.run_pending()