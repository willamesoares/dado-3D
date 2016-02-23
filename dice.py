from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Image import *
import sys
import random as r
import time

#string para identificar quando ESC for pressionado
ESCAPE = '\033'
RETURN = '\r'

#ID da janela GLUT
window = 0

#angulo e coordenadas de rotacao do cubo
angulo = 0.0
xrot = yrot = zrot = 5.0
texCounter = 0

#vertices do cubo
vertices = (
     (1, -1, -1), #0
     (1, 1, -1),  #1
     (-1, 1, -1), #2
     (-1, -1, -1),#3
     (1, -1, 1),  #4
     (1, 1, 1),   #5
     (-1, -1, 1), #6
     (-1, 1, 1)   #7
     )
#diferentes cores para cada superficie
cores = (
     (0.0,1.0,0.0),
     (1.0,0.5,0.0),
     (1.0,0.0,0.0),
     (1.0,1.0,0.0),
     (0.0,0.0,1.0),
     (1.0,0.0,1.0)
     )

#superficies do cubo com quatro pontos
superficies = (
     (0,1,2,3),
     (3,2,7,6),
     (6,7,5,4),
     (4,5,1,0),
     (1,5,7,2),
     (4,0,3,6),
     )

texSuperficies = (
	(0,1,2,3),
	(1,2,3,0),
	(3,0,1,2),
	(2,3,0,1),
	(1,2,3,0),
	(0,1,2,3)
	)

texturas = (
	(0.0, 0.0),
	(1.0, 0.0),
	(1.0, 1.0),
	(0.0, 1.0)
	)
image = []

#carregar texturas das imagens salvas no array
def LoadTextures(index):
	global image

	ix = image[index].size[0]
	iy = image[index].size[1]
	strImage = image[index].tostring("raw", "RGBX", 0, -1)

	glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, strImage)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

#Configurar parametros iniciais da janela
#chamada logo apos criar a janela
def InitGL(width, height):
	#carregar texturas
	LoadTextures(0)
	glEnable(GL_TEXTURE_2D)

	#limpar o fundo com cor preta
	glClearColor(0.0,0.0,0.0,0.0)
	#limpar Depth Buffer
	glClearDepth(1.0)
	#Tipo de teste de profundidade a ser feito
	glDepthFunc(GL_LESS)
	#habilitar teste de profundidade
	glEnable(GL_DEPTH_TEST)
	#habilitar Smooth Color Shading
	glShadeModel(GL_SMOOTH)

	#Calculos de perspectiva

	# GL_PERSPECTIVE_CORRECTION_HINT - especifica a qualidade da cor, textura..
	# Gl_NICEST - escolher opcao de perspectiva mais correta possivel
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	#especifica qual matriz sera afetada pelas linhas seguintes (matriz de projecao)
	glMatrixMode(GL_PROJECTION)
	#substituir matriz atual pela matriz identidade
	glLoadIdentity()                    
	#configurar a perspectiva da matriz de projecao
	#fovy - angulo em graus, na direcao das ordenadas
	#aspect - especifica campo de visao na direcao das abscissas
	#zNear e zFar - especifica o espaco no qual o objeto vai estar visivel
	gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

	#aplicar operacoes seguintes ao modelo de visao da matriz
	glMatrixMode(GL_MODELVIEW)

#Redesenhar janela quando ela for redimensionada
def ReSizeGLScene(width, height):
    #prevenir que tamanho seja igual a zero
    if height == 0:
        height = 1

    # PESQUISAR
    glViewport(0, 0, width, height)

    #similar a InitGL
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

#aumentar velocidade de rotacao quando dado for lancado
# def increaseRotation():
#     global angulo, xrot, yrot, zrot
#     #print "increase ", xrot, yrot, zrot
#     while angulo <= 1000:
#         DrawGLScene()
#         #xrot -= 1
#         #yrot -= 1
#         #zrot -= 1
#         angulo *= 1.01
#         #print angulo
#     # #print "increase ", moveArray[1]
#     # randCoord = r.sample(range(100),3)
#     # while angulo <= 10:
#     #     glRotatef(angulo, x
#     #         randCoord[0]/10, 
#     #         randCoord[1]/10, 
#     #         randCoord[2]/10
#     #         )
#     #     #glTranslatef(0.01,0.0,0.0)
#     #     angulo += 0.1
#     #     #moveArray[1] += 0.0001
#     #     #Enable depth test
#     #     #glEnable(GL_DEPTH_TEST)
#     #     #Accept fragment if it closer to the camera than the former one
#     #     #glDepthFunc(GL_LESS)
#     #     #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#     #     #Cube()
#     #     #pygame.display.flip()
#     #     #pygame.time.wait(10)
#     # #return moveArray

#diminuir velocidade de rotacao para mostrar numero obtido
# def decreaseRotation():
#     global angulo, xrot, yrot, zrot
#     #print "decrease ", xrot, yrot, zrot
#     while angulo >= 0:
#         DrawGLScene()
#         #xrot += 2
#         #yrot += 2
#         #zrot += 2
#         angulo *= 0.99
#     # global angulo
#     # #print "decrease", moveArray[1]
#     # randCoord = r.sample(range(100),3)
#     # while angulo >= 0:
#     #     glRotatef(angulo,
#     #         randCoord[0]/10, 
#     #         randCoord[1]/10, 
#     #         randCoord[2]/10
#     #         )
#     #     #glTranslatef(-0.01,0,-0.0)
#     #     angulo -= 0.1
#     #     #moveArray[1] -= 0.0001
#     #     #Enable depth test
#     #     #glEnable(GL_DEPTH_TEST)
#     #     #Accept fragment if it closer to the camera than the former one
#     #     #glDepthFunc(GL_LESS)
#     #     #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#     #     #Cube()
#     #     #pygame.display.flip()
#     #     #pygame.time.wait(10)
#     # #return moveArray

#Desenhar objetos no ambiente
def DrawGLScene():
    global angulo, xrot, yrot, zrot, texCounter
    #print "draw ", xrot, yrot, zrot
    #limpar tela  e depth buffer p/ evitar rastros
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0,0.0,-10) #afastar objeto no eixo z
    glRotatef(xrot,1.0,0.0,0.0)
    glRotatef(yrot,0.0,1.0,0.0)
    glRotatef(zrot,0.0,0.0,1.0)

    #AREA DE DESENHO--------------------------------------------------	
    #cores podem ser aplicadas por vertice ou por objeto
    #desenhar cubo e aplicar texturas em cada superficie
    for i, superficie in enumerate(superficies):
    	LoadTextures(i)
    	glBegin(GL_QUADS)
        #glColor3fv(cores[i])
        texVertices = texSuperficies[i]
        #desenhar superficie
        for i, vertice in enumerate(superficie):
          	glTexCoord2fv(texturas[texVertices[i]])
          	glVertex3fv(vertices[vertice])
    	glEnd()
    #-----------------------------------------------------------------
    xrot += 1.0
    yrot += 1.0
    zrot += 1.0

    #como ha o uso de buffer duplo, eles devem ser trocados
    #para que o que foi desenhado recentemente seja mostrado
    glutSwapBuffers()
    #time.sleep(0.3)

#Gerenciar teclas pressionadas
def keyPressed(*args):
    global angulo, xrot, yrot, zrot
    global window

    #ESCAPE
    if args[0] == ESCAPE:
        sys.exit()
    if args[0] == RETURN:
        print "processo de lancamento a ser implementado"

def main(*args):
    global window, image

    #verificar argumentos recebidos via cmd
    if len(sys.argv) > 1:
        if sys.argv[1] == "fast" or sys.argv[1] == "slow":
            for i in xrange(1,7):
                image.append(open("textures-" + sys.argv[1] + "/" + `i` + ".jpg"))
        else:
            print "dice.py: opcao invalida", sys.argv[1]
            print "Modo padrao de textura aplicado."
            for i in xrange(1,7):
                image.append(open("textures-fast/" + `i` + ".jpg"))
    else:
        for i in xrange(1,7):
            image.append(open("textures-fast/" + `i` + ".jpg"))

    #passar argumentos para funcao init
    #deve ser chamada antes de glutCreateWindow
    glutInit(sys.argv)

    #configurar modo de display inicial
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    #dimensoes da janela
    glutInitWindowSize(640, 480)

    #posicao inicial da janela
    glutInitWindowPosition(0,0)

    #criar janela, recuperar ID e configurar titulo da janela
    window = glutCreateWindow("Dado 3D")

    #registrar qual funcao ira desenhar
    glutDisplayFunc(DrawGLScene)

    #Funciona como um while loop pra redesenhar o objeto constantemente
    glutIdleFunc(DrawGLScene)

    # Funcao a ser chamada quando janela for redimensionada
    glutReshapeFunc(ReSizeGLScene)

    #Funcao a ser chamada quando alguma tecla for pressionada
    glutKeyboardFunc(keyPressed)

    #inicializar janela
    InitGL(640,480)

    #iniciar evento
    glutMainLoop()

if __name__ == '__main__':
    main()