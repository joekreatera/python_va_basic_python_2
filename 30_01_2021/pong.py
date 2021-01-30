from random import random
bx = 0
by = 0
width = 100
height = 50
p1x = -width/2
p1y = 0
p2x = width/2
p2y = 0
ph= 2
vx = 1
vy = 1
def update(ballX,ballY,velocityX,velocityY,fieldWidth,fieldHeight,player1X,player1Y,player2X,player2Y, playerHeight):
    ballX = ballX + velocityX
    ballY = ballY + velocityY
    if( ballX >= fieldWidth/2):
        velocityX = velocityX*-1
    if( ballX == player2X):
        if( ballY <= (player2Y + playerHeight/2) and ballY >= (player2Y - playerHeight/2)  ):
            velocityX = velocityX*-1
        else:
            print("LOSSSSSSEEEEERRRRRR")
            ballX = 0
            ballY = 0
    if( ballX <= -fieldWidth/2):
        velocityX = velocityX*-1
    if( ballY >= fieldHeight/2):
        velocityY = velocityY*-1
    if( ballY <= -fieldHeight/2):
        velocityY = velocityY*-1
    player1Y = ballY
    dist = (ballY - player2Y)*(random()*0.5+0.5)
    player2Y = player2Y + dist

    return ballX, ballY, velocityX, velocityY, player1Y, player2Y

print("Starting")
i = 0
while i < 300 :
    bx,by,vx,vy,p1y,p2y = update(bx,by,vx,vy,width,height, p1x,p1y, p2x,p2y, ph);
    print(f'b:{bx},{by}  p1:{p1x},{p1y} \t\t p2:{p2x},{p2y}')
    i = i+1
