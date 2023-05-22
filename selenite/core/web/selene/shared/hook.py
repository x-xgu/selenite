import allure


def attach_video_on_failure(video_src: str) -> None:
    body = f"""
    <video 
        controls="" 
        style="max-width: auto; height: 100%;" 
        src="{video_src}" 
        alt="">
        
    </video>
    """
    allure.attach(
        body=body,
        name='video',
        attachment_type=allure.attachment_type.HTML
    )
