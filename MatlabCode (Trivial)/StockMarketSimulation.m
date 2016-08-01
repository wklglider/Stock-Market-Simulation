function varargout = StockMarketSimulation(varargin)
% STOCKMARKETSIMULATION MATLAB code for StockMarketSimulation.fig
%      STOCKMARKETSIMULATION, by itself, creates a new STOCKMARKETSIMULATION or raises the existing
%      singleton*.
%
%      H = STOCKMARKETSIMULATION returns the handle to a new STOCKMARKETSIMULATION or the handle to
%      the existing singleton*.
%
%      STOCKMARKETSIMULATION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in STOCKMARKETSIMULATION.M with the given input arguments.
%
%      STOCKMARKETSIMULATION('Property','Value',...) creates a new STOCKMARKETSIMULATION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before StockMarketSimulation_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to StockMarketSimulation_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help StockMarketSimulation

% Last Modified by GUIDE v2.5 02-Jul-2016 17:59:20

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @StockMarketSimulation_OpeningFcn, ...
                   'gui_OutputFcn',  @StockMarketSimulation_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before StockMarketSimulation is made visible.
function StockMarketSimulation_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to StockMarketSimulation (see VARARGIN)

% Choose default command line output for StockMarketSimulation
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes StockMarketSimulation wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = StockMarketSimulation_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
    data = xlsread('table.csv');
    x = data(:,1);
    adjClose = data(:,7);
    PeriodicDailyReturn = zeros(size(adjClose) - 1);
    for i = 2:numel(adjClose) 
        temp = adjClose(i) / adjClose(i-1);
        PeriodicDailyReturn(i) = log(temp);
    end
    Average = mean2(PeriodicDailyReturn);
    Variance = var(PeriodicDailyReturn,1);
    StandardDeviation = sqrt(Variance);
    Drift = Average - (Variance / 2);
    
    FutureDays = 360;
    FuturePrices = zeros(FutureDays);
    PriceToday = adjClose(numel(adjClose));
    for i = 1:FutureDays
        FuturePrices(i) = PriceToday * exp(Drift + StandardDeviation * norminv(rand,0,1));
        PriceToday = FuturePrices(i);
    end
        
    minY = min(FuturePrices(FuturePrices>0));
    maxY = max(FuturePrices(:));
    minYInt = floor(minY) - 0.05 * minY;
    maxYInt = ceil(maxY) + 0.05 * maxY;
    
    %Chart Output
    axes(handles.axes1);
    plot(FuturePrices);
    axis([0 FutureDays minYInt maxYInt]);
