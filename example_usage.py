import math as m


def distance():
    w=0
    if d ==0 :
        w= (v/0.01)*m.sin(theta_thilde)+ k2*m.tanh(k3*theta_thilde)
    else :
        w= (v/d)*m.sin(theta_thilde)+ k2*m.tanh(k3*theta_thilde)
    return w


def PWM_g(x_actuel, y_actuel, theta, x_consigne, y_consigne):
    #Définition des constantes
    k1 = 1
    k2=1
    k3 = 1
    k_s = 0.045
    v_max= 0.32
    delta = 0.12
    #Calculs des variables
    x_thilde = x_consigne -x_actuel
    y_thilde = y_consigne - y_actuel
    theta_thilde = m.atan2(y_thilde,x_thilde)-theta
    d = m.sqrt(x_thilde*x_thilde +y_thilde*y_thilde)
    v = abs(d/(k1+d)*v_max*m.cos(k3*theta_thilde))

    #Calcul final
    moteur_gauche = -1*(delta/k_s)*((1/2)*distance()+(1/delta)*v)
    moteur_droit = (delta/k_s)*(-(1/2)*distance()*(1/delta)*v)
    return moteur_gauche, moteur_droit

def PWM_d(x_actuel, y_actuel, theta, x_consigne, y_consigne):
    #Définition des constantes
    k1 = 1
    k2=1
    k3 = 1
    k_s = 0.045
    v_max= 0.32
    delta = 0.12
    #Calculs des variables
    x_thilde = x_consigne -x_actuel
    y_thilde = y_consigne - y_actuel
    theta_thilde = m.atan2(y_thilde,x_thilde)-theta
    d = m.sqrt(x_thilde*x_thilde +y_thilde*y_thilde)
    v = abs(d/(k1+d)*v_max*m.cos(k3*theta_thilde))

    #Calcul final
    moteur_droit = (delta/k_s)*(-(1/2)*distance()*(1/delta)*v)
    return moteur_droit
