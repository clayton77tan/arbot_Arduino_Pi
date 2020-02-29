%% Plotting data from ODrive data in .txt Format
% Put file in the same directory of data!
% 02/28/2020

clear vars;
clc;

filename = "Feb_27_19_48.txt"
% make these the correct variable names and size
pos_estimate = [];
pos_setpoint = [];
current_measured = [];
sampling_rate = 20;


path = pwd; 

file_path = strcat(path,'/',filename);
odrv_data = fileread(file_path);

%% Parse the data
odrv_data = extractBetween(odrv_data, '[',']');
index = 1;
data = [];
for i = 1:length(odrv_data)
    test_for_bracket{index} = extractAfter(odrv_data{i},'[');
    if strcmp(test_for_bracket{index},'')
        data{index} = odrv_data{i};
        index = index +1;
    else 
        data{index} = test_for_bracket{index};
        index = index + 1;
        
    end
end

%% Separate by comma
index = 1;
timestep = [];

for i = 1:length(data)
    time_step{index} = strsplit(data{i}, ',');
    pos_estimate(index) = str2double(time_step{i}{1});
    pos_setpoint(index) = str2double(time_step{i}{2});
    current_measured(index) = str2double(time_step{i}{3});
    index = index +1;
end

total = length(time_step)/sampling_rate;
step_size = 1/sampling_rate;
time = step_size:step_size:total;
figure(1)
subplot(3,1,1)
plot(time, pos_estimate)
subplot(3,1,2)
plot(time, pos_setpoint)
subplot(3,1,3)
plot(time, current_measured)

    
        