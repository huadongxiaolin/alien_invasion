import pygame.font


class BUtton:
    def __init__(self, ai_game, msg):
        """初始化按钮属性"""
        # msg是要在按钮上显示的文本
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.buttom_color=(0,255,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        #创建按钮的rect对象，并使其居中
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        #按钮的标签只创建一次
        self._pre_msg(msg)

    def _pre_msg(self,msg):
        """将msg渲染为图像,并使其在按钮上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color
                                        ,self.buttom_color)
        #布尔实参指定开启还是关闭反锯齿功能，反锯齿让文本的边缘更平滑
        self.msg_image_rect=self.msg_image.get_rect()
        #让图像文本在按钮上居中
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.buttom_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
