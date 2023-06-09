from vpython import *

# power 35-40 정도면 인게임에서 구석으로 꽂힘
# 여기서도 35-40이면 들어감

# ball2dpos = ball 정사영
# eye2dpos = eye 정사영
 
import random

scene = canvas(width = 1400, height = 600, title = "피파온라인4")
scene.background = color.white

# constants
g = 9.8
rho = 1.204 # air density
Cd = 0.3 # air resistance
Cm = 1 # air magnus
w = 15*pi #각속도

def shootbtn(b) :
    b.disabled=True
    return b.disabled

    
def shoot_directd(direct_d) :

    # direct_d have no deceleration in the given power
    ball.v = direct_d*hat(shootvec)+vec(0,direct_d/5,0)
    
    dt = 0.01
    t = 0
    
    while t<2.5 :
        rate(1/dt)
        ball.v+=vec(0,-g*ball.m,0)*dt
        ball.pos += ball.v*dt
        
        t+=dt
        
        
def shoot_rightzd(right_zd) :
    
    ball.v = right_zd/2*hat(shootvec)+vec(right_zd/3,right_zd/3,-right_zd/4)
    
    dt = 0.01
    t = 0
    
    while t<2.5 : 
        rate(1/dt)
        
        Fg = vec(0,-g*ball.m,0)
        Fd = -0.5*Cd*rho*(pi*ball.r**2)*mag(ball.v)**2*hat(ball.v)
        Fm = 0.5*Cm*rho*(pi*ball.r**2)*ball.r*mag(ball.v)*w*cross(vec(0,1,0),hat(ball.v))
    
        Fnet = Fg+Fd+Fm
        ball.a = Fnet/ball.m
        
        ball.v+=ball.a*dt
        ball.pos+=ball.v*dt

        t+=dt
        
def shoot_leftzd(left_zd) :

    ball.v = left_zd/2*hat(shootvec)+vec(-left_zd/3,left_zd/3,-left_zd/4)
    
    dt = 0.01
    t = 0
    
    while t<2.5 : 
        rate(1/dt)
        
        Fg = vec(0,-g*ball.m,0)
        Fd = -0.5*Cd*rho*(pi*ball.r**2)*mag(ball.v)**2*hat(ball.v)
        Fm = 0.5*Cm*rho*(pi*ball.r**2)*ball.r*mag(ball.v)*w*cross(vec(0,-1,0),hat(ball.v))
    
        Fnet = Fg+Fd+Fm
        ball.a = Fnet/ball.m
        
        ball.v+=ball.a*dt
        ball.pos+=ball.v*dt
        
        t+=dt
        
# setting
    
ground = box(pos=vec(0,0,0),size=vec(50,0.1,50),color=color.green)

# box center = mid position -> if height changes pos.y have to change
post1 = box(pos=vec(-4,2,-20),axis=vec(1,0,0),size=vec(0.5,4,2),color=color.red) # left post
post2 = box(pos=vec(4,2,-20),axis=vec(1,0,0),size=vec(0.5,4,2),color=color.red) # right post
post3 = box(pos=vec(0,4.25,-20),axis = vec(1,0,0),size=vec(8.5,0.5,2),color=color.red) # top post

# post center 정사영
post2dpos = vec(0,0,-20)

btnShoot = button(text="shoot",bind=shootbtn)

goal_label = label(pos=scene.center+vec(0,1,0),box=False,height = 30,text='GOAL!',color=color.blue,visible = False)
miss_label = label(pos=scene.center+vec(0,2,0),box=False,height=30,text='Miss wide!',color=color.blue,visible =False)

while True :
    ball = sphere(pos=vec(random.randint(-15,15),0.3,random.randint(8,15)),radius=0.3,color=color.white)
    ball.m = 1
    ball.r = 0.2

    ball2dpos = ball.pos - vec(0,0.3,0)

    eyedir = hat(ball2dpos-post2dpos)
    eye2dpos = vec(ball.pos.x/(ball.pos.z+20)*(18+20),0,18)
    eyepos = eye2dpos + vec(0,2,0)


    shootdir = arrow(pos=ball2dpos,axis=4*hat(ball2dpos-eye2dpos),shaftwidth=0.15,color=color.black)

    scene.camera.pos = eyepos
    scene.camera.axis = shootdir.axis

    angle = radians(1)
    axis = vec(0,1,0)
    origin = ball.pos

    while btnShoot.disabled==False :

        rate(100)
    
        if btnShoot.disabled : break

        s = keysdown()
        print("You pressed the key", s)  
    
        if 'left' in s: 
            scene.camera.rotate(angle=radians(1), axis=axis, origin=origin)
            shootdir.axis=6*hat(scene.camera.axis)
        if 'right' in s: 
            scene.camera.rotate(angle=radians(-1), axis=axis, origin=origin)
            shootdir.axis=6*hat(scene.camera.axis)

    
    # the most important variable
    # used in final shooting
    shootvec = shootdir.axis

    right_zd = 0
    left_zd = 0
    direct_d = 0

    dpower = 1 # power+=dpower

    scene.waitfor('keydown')

    while btnShoot.disabled :
        rate(100)  # Limit the loop rate for smooth animation
    
        s = keysdown()  # Get the keys that are currently pressed
    
        print(s)
        if 'z' in s and 'right' in s :
            right_zd += dpower
            print("right zd Power :", right_zd)
        else if 'z' in s and 'left' in s :
            left_zd += dpower
            print("left zd Power :", left_zd)
        else if 'q' in s and 'd' in s :
            direct_d +=dpower
            print("direct shoot :",direct_d)
        else if s==[] :
            break

    if right_zd > 0 :
        shoot_rightzd(right_zd)
    else if left_zd > 0 :
        shoot_leftzd(left_zd)
    else if direct_d > 0 :
        shoot_directd(direct_d)
        
    scene.waitfor('click')
    goal_label.visible = False
    miss_label.visible = False
    btnShoot.disabled = False
    ball.visible = False
    shootdir.visible = False