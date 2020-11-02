from pyjoycon import JoyCon, get_R_id, get_L_id

joycon_R_id = get_R_id()
joycon_R = JoyCon(*joycon_R_id)
print(joycon_R.get_status())

# joycon_L_id = get_L_id()
# joycon_L = JoyCon(*joycon_L_id)
# print(joycon_L.get_status())

from pyjoycon import GyroTrackingJoyCon, get_R_id
import time
from LivePlot import LivePlot as LP

joycon_id = get_R_id()
joycon = GyroTrackingJoyCon(*joycon_id)

dict_data = {'t': [],
             'Px': [],
             'Py': [],
             'Rx': [],
             'Ry': [],
             'Rz': [],
             'Dx': [],
             'Dy': [],
             'Dz': []}

if __name__ == '__main__':
    
    # freeze_support()
    app = LP.LivePlotApp(data_format=dict_data, app_name="JoyCon_data")
    f1 = app.add_figure(title="Pointer", plot_width=300, plot_height=300)
    app.add_line_to_figure(f1, "t", "Px", line_color="blue")
    app.add_line_to_figure(f1, "t", "Py", line_color="orange")

    f2 = app.add_figure(title="Rotation", plot_width=300, plot_height=300)
    app.add_line_to_figure(f2, "t", "Rx", line_color="blue")
    app.add_line_to_figure(f2, "t", "Ry", line_color="orange")
    app.add_line_to_figure(f2, "t", "Rz", line_color="green")

    f3 = app.add_figure(title="Direction", plot_width=300, plot_height=300)
    app.add_line_to_figure(f3, "t", "Dx", line_color="blue")
    app.add_line_to_figure(f3, "t", "Dy", line_color="orange")
    app.add_line_to_figure(f3, "t", "Dz", line_color="green")

    time.sleep(1)
    app.start_process()

    while True:
        time.sleep(0.05)
        t = time.perf_counter()
        dict_data['t'] = [t]
        jp = joycon.pointer
        jr = joycon.rotation
        jd = joycon.direction
        if jp and jr and jd:
            dict_data['Px'] = [jp[0]]
            dict_data['Py'] = [jp[1]]
            dict_data['Rx'] = [jr[0]]
            dict_data['Ry'] = [jr[1]]
            dict_data['Rz'] = [jr[2]]
            dict_data['Dx'] = [jd[0]]
            dict_data['Dy'] = [jd[1]]
            dict_data['Dz'] = [jd[2]]
            app.parent_conn.send(dict_data)
