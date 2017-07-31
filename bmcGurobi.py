from __future__ import print_function
import gurobipy
import sys

class GRBEncoder:
    def __init__(self, t_end):
        self.__t_end = t_end
        self.__n = t_end//5
        self.__g = {}
        self.__iob = {}
        self.__id = {}
        self.__int = {}
        self.__ip = {}
        self.__saturation = {}
        self.Ti = 160.0 # 160.0
        self.Td = 60.0 # 60.0
        self.Kp = 0.05 # 0.023
        self.K1 = 0.5
        self.K2 = 0.25
        self.K0 = 0.75
        self.gamma = 0.5 # 0.5
        self.Ki = self.Kp/self.Ti
        self.Kd = self.Kp * self.Td / 5.0
        self.target = 100
        self.glucose_lb = 0
        self.glucose_ub = 500
        self.max_gluc_change = 10
        self.min_gluc_change = -10
        self.past_iob_max = 4.0
        self.past_iob_min = 0.5
        self.past_gluc_max = 180
        self.past_gluc_min = 80
        self.glucose_eq_step1 = 5
        self.glucose_eq_step2 = 5
        self.glucose_eq_step3 = 5
        self.iob_max = 10.0
        self.id_max = 20.0
        self._mdl = gurobipy.Model('test') #takes desired model name as its argument (eg test)

    # Phase 1 : Create all the variables we will need
    def create_all_variables(self):
        for i in range(0, self.__t_end+5, 5):
            self.__g[i] = self._mdl.addVar(lb=self.glucose_lb, ub=self.glucose_ub, obj=0.0,
                                           vtype=gurobipy.GRB.CONTINUOUS, name='G_%d' % i)

            self.__iob[i] = self._mdl.addVar(name='IOB_%d' % i, vtype=gurobipy.GRB.CONTINUOUS,
                                             lb=0.0, ub=self.iob_max, obj=0.0)
            self.__id[i] = self._mdl.addVar(name='I_D_%d' % i, vtype=gurobipy.GRB.CONTINUOUS,
                                            lb=0.0, ub=self.id_max)
            self.__int[i] = self._mdl.addVar(name='INT_ERROR_%d' % i, vtype=gurobipy.GRB.CONTINUOUS)
            self.__ip[i] = self._mdl.addVar(name="Insulin_Pred_%d" % i, vtype=gurobipy.GRB.CONTINUOUS,
                                            lb=0.0)
            self.__saturation[i] = self._mdl.addVar(name='W_%d' % i, vtype=gurobipy.GRB.BINARY)

    def create_past_variables_and_constraints(self, look_back):
        self.__past_iob = self._mdl.addVar(name="past_iob", vtype=gurobipy.GRB.CONTINUOUS,
                                           lb = self.past_iob_min, ub = self.past_iob_max)
        for i in range(-look_back, 0, 5):
            self.__g[i] = self._mdl.addVar(name="G_Past_%d"%(-i), vtype=gurobipy.GRB.CONTINUOUS,
                                           lb = self.past_gluc_min, ub = self.past_gluc_max)
            self.__iob[i] = self.__past_iob
        self.__id[-5] = 0.0
        self.__id[-10] = 0.0
        self.__ip[-5] = 0.0
        self.__ip[-10] = 0.0

    def __get_from_map(self, m, t):
        assert t in m
        return m[t]

    def g(self, t):
        return self.__get_from_map(self.__g, t)

    def iob(self, t):
        return self.__get_from_map(self.__iob, t)

    def id(self, t):
        return self.__get_from_map(self.__id, t)

    def int_error(self, t):
        return self.__get_from_map(self.__int, t)

    def ip(self, t):
        return self.__get_from_map(self.__ip, t)

    def saturation(self, t):
        return self.__get_from_map(self.__saturation, t)

    def add_glucose_change_bounds(self):
        for i in range(0, self.__t_end+5, 5):
            self._mdl.addConstr(self.g(i) - self.g(i-5) <= self.max_gluc_change)
            self._mdl.addConstr(self.g(i) - self.g(i-5) >= self.min_gluc_change)

    def add_glucose_equation(self, a1, a2, a3, deltaG, deltaI, e_min, e_max, e_mean, step=5):
        for i in range(0, self.__t_end+5, step):
            if i + deltaG <= self.__t_end:
                # G(i+deltaG) - a1 G(i) - a2 G(i - deltaG) - a3 IOB(i - deltaI) <= e_max
                # G(i+deltaG) - a1 G(i) - a2 G(i - deltaG) - a3 IOB(i - deltaI) >= e_min

                self._mdl.addConstr(
                    self.g(i+deltaG) - a1 * self.g(i) - a2 * self.g(i-deltaG) \
                    - a3 * self.iob(i-deltaI)  <= e_mean + e_max
                )
                self._mdl.addConstr(
                    self.g(i+deltaG) - a1* self.g(i) - a2* self.g(i-deltaG) \
                    - a3 * self.iob(i-deltaI) >= e_mean + e_min
                )

    def add_iob_equations(self):
        # IOB(t) = 1.89 IOB(t-5) - 0.9 IOB(t-10) + Id(t) - 0.9 Id(t-5) + 0.002 Id(t-10)
        for i in range(0, self.__t_end+5, 5):
            self._mdl.addConstr(self.iob(i) == 1.89 * self.iob(i-5)  \
                                - 0.9 * self.iob(i-10) + self.id(i) * 1/12 \
                                - 0.9 * self.id(i-5) * 1/12 + 0.002 * self.id(i-10) *1/12)

    # Phase 3  : Set up the initial conditions
    def setup_controller_equations(self):
        for i in range(0, self.__t_end+5, 5):
            err_term = self.g(i) - self.target
            p_expr = self.Kp * err_term
            if i >= 5:
                i_expr = self.int_error(i-5) + self.Ki * err_term
            else:
                i_expr = 0.0
            self._mdl.addConstr(self.int_error(i) == i_expr)
            g_diff = self.g(i) - self.g(i-5)
            d_expr = self.Kd * g_diff
            ip_update_expr = self.K0 * self.id(i-5) + self.K1 * self.ip(i-5) \
                             - self.K2 * self.ip(i-10)
            self._mdl.addConstr(self.ip(i) == ip_update_expr)
            pid_expr = p_expr + i_expr + d_expr
            raw_id = pid_expr - self.gamma * self.ip(i)
            self._mdl.addConstr(self.id(i) >= raw_id)
            self._mdl.addConstr(self.id(i) <= raw_id + self.id_max * self.saturation(i))
            self._mdl.addConstr(self.id(i) <= self.id_max - self.id_max * self.saturation(i))
            self._mdl.addConstr(self.id(i) >= 0.0)

    def setup(self):
        self.create_all_variables()
        #self.add_bounds_to_vars()
        self.create_past_variables_and_constraints(120)
        self.add_glucose_change_bounds()
        # -- BEGIN OLD MODEL first pass--
        # (a(1) a(2) a(3) DeltaG DeltaI minus95 plus95 stdev )
        # self.add_glucose_equation(0.363, 0.594, -2.25, 30, 30, -6, 6, 1.1)
        # self.add_glucose_equation(0.382, 0.675, -13.35, 45, 45, -7.5, 7.5, 1.4)
        # self.add_glucose_equation(0.516, 0.52, -13.3, 60, 60, -2.5, 2.5, 0.5)
        # self.add_glucose_equation(0.461, 0.467, -17.01, 120, 120, -4, 4, 0.9 )
        # -- BEGIN NEW MODEL global --
        #self.add_glucose_equation(-0.2324, 1.2047, -1.7098, 30, 30, -40, 40, 18.8)
        #self.add_glucose_equation(0.0940, 0.9315, -4.0147, 30, 30, -28, 28, 13)
        #self.add_glucose_equation(0.1605, 0.9024, -7.452, 45, 45, -34, 34, 16)
        #self.add_glucose_equation(0.2215, 0.8531, -7.89, 60, 60,-40, 40, 18.34)
        #self.add_glucose_equation(0.4747, 0.7077, -7.935, 120, 120, -48, 48, 21.25)
        # -- BEGIN NEW MODEL window --
        #self.add_glucose_equation(0.4937, 0.5582, -3.4635, 30, 30, -11, 11, 5.6) #30Win100
        #self.add_glucose_equation(0.2332, 0.7945, -3.7159, 30, 30, -20, 20, 10.3) #30Win200
        #self.add_glucose_equation(0.5415, 0.6144, -13.5804, 45, 45, -3.3, 3.3, 1.7) #45Win100
        #self.add_glucose_equation(0.4192, 0.6847, -11.3894, 45, 45, -21, 21, 10.7) #45Win200
        #self.add_glucose_equation(0.4673, 0.6404, -10.8473, 60, 60, -17.4, 17.4, 8.8) #60win200
        self.add_glucose_equation(0.3654, 0.7140, -9.8856, 60, 60, -23.1, 23.1, 11.8) #60win300
        self.add_iob_equations()
        self.setup_controller_equations()

    def extract_solution(self):
        assert self._mdl.status == gurobipy.GRB.OPTIMAL
        print('Found solution with objective: ', self._mdl.objVal)
        print('Time, ', 'Glucose, ', 'IOB', 'ID')
        for i in range(0, self.__t_end+5, 5):
            print(i, ', ', self.g(i).x, ', ', self.iob(i).x, ',', self.id(i).x)
        return self._mdl.objVal

    def solve_for_glucose(self, oFile):
        print('Minimizing Glucose')
        self._mdl.setObjective(self.g(self.__t_end), gurobipy.GRB.MINIMIZE)
        self._mdl.optimize()
        if self._mdl.status == gurobipy.GRB.OPTIMAL:
            value = self.extract_solution()
            print(self.__t_end, value, sep=' , ', end='', file=oFile)
        print('Maximizing Glucose')
        self._mdl.setObjective(self.g(self.__t_end), gurobipy.GRB.MAXIMIZE)
        self._mdl.optimize()
        if self._mdl.status == gurobipy.GRB.OPTIMAL:
            value = self.extract_solution()
            print(',', value, file=oFile)

def main(argv):
    if len(argv) < 3:
        print('Usage: python ', sys.argv[0], '[Depth to Explore]  [Output file]')
    d = int(sys.argv[1])
    oFile = open(sys.argv[2], 'a')
    for depths in range(0, d, 10):
        g = GRBEncoder(depths)
        g.setup()
        g.solve_for_glucose(oFile)
    print('DONE')
    oFile.close()

if __name__ == '__main__':
    main(sys.argv)
