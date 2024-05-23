import json
import pytest
import project.baseplate_KDS41_30_2022.baseplate_KDS41_30_2022_calc

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def test_baseplate_KDS41_30_2022_calc():
    input = {'B' : 1000, 'H' : 10000, 'Fc' : 24 , 'Fy' : 400,
             'Ec' : 25811.006260943130 , 'Es' : 210000,  
             'bolt' : [
                {'X' : 90, 'Y' : 0, 'Area' : 314.15926535897933 },
                { 'X' : -90, 'Y' : 0, 'Area' : 314.15926535897933 }],
              'P' : 30000, 'Mx' : 0, 'My' : 100000000.0
            }

    JsonData = json.dumps(input)
    result = project.baseplate_KDS41_30_2022.baseplate_KDS41_30_2022_calc.calc_ground_pressure(JsonData)
    data_sets = result['concrete']

    # 중앙점과 압력 값 계산
    centers_x = []
    centers_y = []
    pressures = []

    for data in data_sets:
        x = np.array([data['Node1'][0], data['Node2'][0], data['Node3'][0], data['Node4'][0]])
        y = np.array([data['Node1'][1], data['Node2'][1], data['Node3'][1], data['Node4'][1]])
        pressure = data['Pressure'] * 1000

        center_x = np.mean(x)
        center_y = np.mean(y)

        centers_x.append(center_x)
        centers_y.append(center_y)
        pressures.append(pressure)

    max_pressure = max(pressures)
    max_index = pressures.index(max_pressure)
    max_center_x = centers_x[max_index]
    max_center_y = centers_y[max_index]


    # 선형 보간을 통해 그리드 데이터 생성
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(centers_x, centers_y, c=pressures, cmap='viridis', s=100, edgecolors='k')
    plt.colorbar(scatter, label='Pressure')
    plt.text(max_center_x, max_center_y, f'  {round(max_pressure)}', horizontalalignment='left', verticalalignment='center', fontsize=12, color='black')

    plt.grid(True)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Pressure Visualization at Center Points')
    plt.show()

    assert pytest.approx(result['bolt'][0]['Load']) == 0.0
    assert pytest.approx(result['bolt'][1]['Load']) == -269182.84245616524
    
    

test_baseplate_KDS41_30_2022_calc()