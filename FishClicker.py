from PyWigit import *
screen = NewScreen((720, 400))
font = NewFont("timesnewroman", 20)
SetCaption("Button Clicker")
cash = 0
Buttons = []
def Button0Click():
    global cash
    if Buttons[0][1] <= cash:
        cash -= Buttons[0][1]
        cash += Buttons[0][2]
        Buttons[0][3] += 1
i = 1
def NewUpgrade():
    global i
    exec(f"""def Button{i}Click():
    global cash
    if Buttons[{i}][1] <= cash:
        cash -= Buttons[{i}][1]
        Buttons[{i-1}][2] += Buttons[{i}][2]
        Buttons[{i}][1] = int(Buttons[{i}][1] * 1.1)
        if Buttons[{i}][3] == 0:
            NewUpgrade()
        Buttons[{i}][3] += 1
Buttons.append([Button(font.render("Button {i+1}($.): .", True, White), LeftClick=Button{i}Click), 10**(i+1), 1, 0])
""")
    i+=1
Buttons.append([Button(font.render("Button: .", True, White), LeftClick=Button0Click), 0, 1, 0])
NewUpgrade()
def DrawFunc(screen):
    screen.blit(font.render("CASH: "+ str(cash), True, White), (20, 0))
    Buttons[0][0].display = font.render(f"Button: {Buttons[0][3]}, {Buttons[0][2]} per click", True, White)
    Buttons[0][0].draw(screen, (20, 20))
    Buttons[1][0].display = font.render(f"Button 2(${Buttons[1][1]}): {Buttons[1][3]}, Increase Button value by {Buttons[1][2]} per click", True, White)
    Buttons[1][0].draw(screen, (20, 40))
    for i in range(2, len(Buttons)):
        Buttons[i][0].display = font.render(f"Button {i+1}(${Buttons[i][1]}): {Buttons[i][3]}, Increase Button {i} value by {Buttons[i][2]} per click", True, White)
        Buttons[i][0].draw(screen, (20, 20+20*i))
def InputFunc(event):
    for i in range(len(Buttons)):
        if Buttons[i][0].Click(event):
            return True
CreateScrn(DrawFunc, InputFunc, Black)
Screen(screen, FullScreen=True)
while Status():
    MainLoop(screen)
pygame.quit()
