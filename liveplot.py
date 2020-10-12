from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from tornado import gen
from tornado.ioloop import IOLoop
from multiprocessing import Process, Pipe

class LivePlotApp(object):
    parent_conn, child_conn = Pipe()

    def __init__(self, data_format, app_name = 'myapp', update_step_ms = 1, stream_rollover = 50):
        self.app_name = app_name
        self.data_format = data_format
        self.update_step_ms = update_step_ms
        self.stream_rollover = stream_rollover
        self.figs = []
        self.lines = []
        self.figs_n = 0

    def start_process(self):
        self.process = Process(target = self.start_io_loop, args=(self.child_conn,), daemon=True)
        self.process.start()

    # Safe update
    @gen.coroutine
    def locked_update(self):
        try:
            x = self.cc.recv() # This is blocking
        except EOFError:
            pass
        self.source.stream(x, rollover = self.stream_rollover)

    def start_io_loop(self, child_conn):
        self.io_loop = IOLoop.current()
        self.server = Server(applications = 
                                {'/'+self.app_name: Application(FunctionHandler(self.make_document))}, 
                                    io_loop = self.io_loop, 
                                    port = 5001)
        self.server.start()
        self.server.show('/'+self.app_name)
        self.cc = child_conn
        self.io_loop.start()

    def make_document(self, doc):
        # Define data source
        self.source = ColumnDataSource(self.data_format)

        # Add figures and lines to plots to document
        figs = []
        for f in self.figs:
            fig = figure(**f)
            figs.append(fig)
        for line in self.lines:
            for fig_n, params in line.items():
                figs[fig_n].line(*params[0], **params[1], source = self.source)
        for f in figs:
            doc.add_root(f)
        
        ##########################################################
        fig1 = figure(title = "FIG 1")
        fig1.line("t", "x", line_color="pink", source=self.source)
        fig1.line("t", "y", line_color="red", source=self.source)
        fig1.line("t", "z", line_color="blue", line_width=2, source=self.source)
        doc.add_root(fig1)
        fig2 = figure(title = "FIG 2")
        fig2.line('t','other', source=self.source)
        doc.add_root(fig2)
        ##########################################################
        
        doc.add_periodic_callback(self.locked_update, self.update_step_ms)

    def add_figure(self, **kwargs):
        self.figs.append(kwargs)
        self.figs_n +=1
        return self.figs_n-1
    
    def add_line_to_figure(self, f, *args, **kwargs):
        self.lines.append({f: (args, kwargs)})

if __name__ == '__main__':
    # Example usage
    import time
    import random
    import math
    dict_data = {'t': [], 'x': [], 'y': [], 'z': [], 'other': []}
    app = LivePlotApp(data_format = dict_data, app_name="Demo_app")
    f1 = app.add_figure(title = "Fig 1", plot_width = 300, plot_height = 300)
    app.add_line_to_figure(f1, "t", "y", line_color="pink")
    app.add_line_to_figure(f1, "t", "z", line_color="red", line_width = 2)
    app.add_line_to_figure(f1, "t", "x", line_color="blue")
    app.add_line_to_figure(f1, "t", "x")
    f2 = app.add_figure(title = "Fig 2", plot_width = 300, plot_height = 300)
    app.add_line_to_figure(f2, "t", "other", line_color="blue")
    
    app.start_process()
    i = 0
    dt = 0.01 # Send data at 100Hz
    t_sent = time.perf_counter()

    while True:
        time.sleep(0.1)
        t = time.perf_counter()
        dict_data['other'] =  [random.randint(1,50)]
        dict_data['t'] = [time.perf_counter()],
        dict_data['x'] = [7 if i<110 else 15]
        dict_data['y'] = [i%100]
        dict_data['z'] = [10+10*math.sin(t*2*math.pi)]
        if (t-t_sent > dt):
            t_sent = time.perf_counter()
            app.parent_conn.send(dict_data)
            i+=1
