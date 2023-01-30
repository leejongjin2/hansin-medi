from hwiUtils.info import info_start, info_end

def inference():
    info_start('inference hanshin')
    
    """_summary_
    모델 존재하는지 체크
    get 일일검진자TB where 발병확률예측컬럼 = null
    for 검진자 in 검진자s :
        inference(검진자)
        update 일일검진자TB where 검진자정보
    """
    info_end('inference hanshin')