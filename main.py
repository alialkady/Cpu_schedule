import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def loop_burst(burst, gnatt, time):
    j = 1
    for i in range(len(burst)):
        if burst[i] > 0:
            if burst[i] > quantum:
                time += quantum
                burst[i] = max(burst[i] - quantum, 0)
                gnatt[j].append(time)
                if i == len(burst) - 1 and burst[0] != 0:
                    gnatt[1].append(time)
                elif i == len(burst) - 1 and burst[0] == 0:
                    pass
                elif burst[i + 1] == 0:
                    pass
                else:
                    gnatt[j + 2].append(time)
            else:
                time += burst[i]
                burst[i] = 0
                gnatt[j].append(time)
                if i == len(burst) - 1 and burst[0] != 0:
                    gnatt[1].append(time)
                elif i == len(burst) - 1 and burst[0] == 0:
                    pass
                elif burst[i + 1] == 0:
                    pass
                else:
                    gnatt[j + 2].append(time)
        j += 2
    return time

def run_round_robin():
    global time_counter
    global burst_times
    global quantum
    global gnatt_time
    result_text = ""
    while any(burst_times):
        time_counter = loop_burst(burst_times, gnatt_time, time_counter)
        result_text += "Burst times after this round of scheduling: {}\n".format(burst_times)
    result_label.config(text=result_text)

def submit_burst_time():
    try:
        burst_time = int(entry_burst_time.get())
        if burst_time < 0:
            entry_burst_time.config(state=tk.DISABLED)
            entry_quantum.config(state=tk.NORMAL)
            btn_submit_quantum.config(state=tk.NORMAL)
            entry_quantum.focus()
        else:
            burst_times.append(burst_time)
            gnatt_time.append(burst_time)
            gnatt_time.append([])
            listbox_burst_times.insert(tk.END, burst_time)
            entry_burst_time.delete(0, tk.END)

        gnatt_time[1] = [0]
    except ValueError:
        pass

def submit_quantum():
    global quantum
    quantum = int(entry_quantum.get())
    run_round_robin()

def plot_gantt_chart(processes):
    fig, ax = plt.subplots()

    # Disable y-axis
    ax.yaxis.set_visible(False)

    # Plotting processes
    labels = []
    colors = []
    for i in range(0, len(processes), 2):
        burst_time = processes[i]
        time_range = processes[i + 1]

        # Assigning different colors to each process
        color = plt.cm.get_cmap('tab10')(i // 2)
        labels.append(f'Process {i // 2}')
        colors.append(color)

        # Plotting the bars for each time range of the process
        for j in range(0, len(time_range), 2):
            start_time = time_range[j]
            end_time = time_range[j + 1]
            ax.barh(i // 2, end_time - start_time, left=start_time, height=0.5, color=color, alpha=0.8)

    # Setting x-axis label
    ax.set_xlabel('Time')

    # Creating custom legend with process numbers
    custom_legend = [mpatches.Patch(color=color, label=f'{label}: Process {i // 2}') for i, (color, label) in
                     enumerate(zip(colors, labels))]
    ax.legend(handles=custom_legend, loc='upper right', bbox_to_anchor=(1.2, 1))

    plt.show()




burst_times = []
gnatt_time = []
quantum = 0
time_counter = 0
root = tk.Tk()
root.title("Round Robin CPU Scheduler")
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

label_burst_time = tk.Label(frame_input, text="Enter burst time (negative to end):")
label_burst_time.grid(row=0, column=0, padx=5, pady=5)

entry_burst_time = tk.Entry(frame_input)
entry_burst_time.grid(row=0, column=1, padx=5, pady=5)
entry_burst_time.focus()

btn_submit_burst_time = tk.Button(frame_input, text="Submit", command=submit_burst_time)
btn_submit_burst_time.grid(row=0, column=2, padx=5, pady=5)

listbox_burst_times = tk.Listbox(frame_input, width=20, height=5)
listbox_burst_times.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

label_quantum = tk.Label(frame_input, text="Enter quantum number:")
label_quantum.grid(row=2, column=0, padx=5, pady=5)

entry_quantum = tk.Entry(frame_input, state=tk.DISABLED)
entry_quantum.grid(row=2, column=1, padx=5, pady=5)

btn_submit_quantum = tk.Button(frame_input, text="Submit", command=submit_quantum, state=tk.DISABLED)
btn_submit_quantum.grid(row=2, column=2, padx=5, pady=5)

result_label = tk.Label(root, text="")
result_label.pack(padx=10, pady=10)

root.mainloop()
plot_gantt_chart(gnatt_time)

