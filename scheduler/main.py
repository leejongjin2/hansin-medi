import schedule
import datetime
from hwiUtils.SchedulerDatabase import HanshinDatabase
from hwiUtils.train import train_HanshinModel, train_InfinityModel
from hwiUtils.inference import inference

def updateModel():
    # Update HanshinTrainTB, InfinityTrainTB Quarterly and Train New Models
    # 분기업데이트 되었는지 확인 추가
    # and day = 1일
    
    hanshinDB = HanshinDatabase()
    
    if (datetime.datetime.now().month % 3 == 1 ):
        # hanshinDB.update_hanshinTrainTB()
        # hanshinDB.update_infinityTrainTB()
        
        hanshinDB.update_outlierTB()
        
        
        hanshin_trainData = hanshinDB.get_hanshinTrainData()
        train_HanshinModel()
        infinity_trainData = hanshinDB.get_infinityTrainData()
        train_InfinityModel()
    
    # Update Hanshin Inference data Everyday and Inference with updated data
    hanshinDB.update_hanshinInferenceTB()
    inference()
    
    hanshinDB.close_db()

if __name__ == "__main__":
    # HH:MM:SS에 작업 실행 -> 매 00시 1분에 실행
    # schedule.every().day.at("14:45:50").do(updateDatabase)
    schedule.every(5).seconds.do(updateModel)
    while 1:
        schedule.run_pending()