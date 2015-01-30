########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.05.December.2014
########################################################################
# This contains postprocessing routines for the DES model.
# Much of this are plots.
# The general plot function has input files.
# These are removed here because there will be a lot of plots.
# The plotting options are hard coded in. 
########################################################################
#
#
#
####### imports
import numpy
import os
import matplotlib
import matplotlib.pyplot as plot
from matplotlib.ticker import MultipleLocator
########################################################################
#
#
#
####### set font size for lables
matplotlib.rcParams.update({'font.size': 14})
#######
#
#
#
########################################################################
#
#
#
####### make plots
### this is the function for the plots that is called in the main file
def make_plots(operation_time,total_campaign,storage_inventory_start,total_melter_failure,system_false_alarm_counter,home_dir,output_data_dir,output_figure_dir):
###
#
### open data files
    total_campaign_graph,true_storage_inventory_graph,expected_storage_inventory_graph,measured_storage_inventory_graph,true_weight_graph,expected_weight_graph,measured_weight_graph,true_processed_inventory_graph,expected_processed_inventory_graph,measured_processed_inventory_graph,true_muf_graph,expected_muf_graph,measured_muf_graph,total_melter_failure_graph,system_false_alarm_counter_graph,true_kmp0_graph,true_kmp1_graph,true_kmp2_graph,true_kmp3_graph,true_kmp4_graph,expected_kmp0_graph,expected_kmp1_graph,expected_kmp2_graph,expected_kmp3_graph,expected_kmp4_graph,measured_kmp0_graph,measured_kmp1_graph,measured_kmp2_graph,measured_kmp3_graph,measured_kmp4_graph,true_heel_graph,expected_heel_graph,measured_heel_graph,true_system_inventory_graph,expected_system_inventory_graph,measured_system_inventory_graph,system_false_alarm_threshold_graph=make_files_for_plot(home_dir,output_data_dir)
###
#
### change to figure dir
    os.chdir(output_figure_dir)
###
#
### these are used to set the maximum y-axis
    true_muf=numpy.max(true_muf_graph[:,1])
    expected_muf=numpy.max(expected_muf_graph[:,1])
    measured_muf=numpy.max(measured_muf_graph[:,1])
#
    true_throughput=numpy.max(true_weight_graph[:,1])
    expected_throughput=numpy.max(expected_weight_graph[:,1])
    measured_throughput=numpy.max(measured_weight_graph[:,1])
#
    true_processed=numpy.max(true_processed_inventory_graph[:,1])
    expected_processed=numpy.max(expected_processed_inventory_graph[:,1])
    measured_processed=numpy.max(measured_processed_inventory_graph[:,1])   
#
    true_system=numpy.max(true_system_inventory_graph[:,1])
    expected_system=numpy.max(expected_system_inventory_graph[:,1])
    measured_system=numpy.max(measured_system_inventory_graph[:,1])
#
    true_heel=numpy.max(true_heel_graph[:,1])
    expected_heel=numpy.max(expected_heel_graph[:,1])
    measured_heel=numpy.max(measured_heel_graph[:,1])
#    
    true_buffer_max=numpy.max(true_storage_inventory_graph[:,1])
    expected_buffer_max=numpy.max(expected_storage_inventory_graph[:,1])
    measured_buffer_max=numpy.max(measured_storage_inventory_graph[:,1])
    true_buffer_min=numpy.min(true_storage_inventory_graph[:,1])
    expected_buffer_min=numpy.min(expected_storage_inventory_graph[:,1])
    measured_buffer_min=numpy.min(measured_storage_inventory_graph[:,1])
#
    system_false_alarm_threshold=numpy.max(system_false_alarm_threshold_graph[:,1])
###
#
### set axes
    xmin_time=-0.50
    xmax_time=(operation_time+0.50)
    xmajortick_time=2
    xminortick_time=1
###
#
### total campaign
    campaign_plot(total_campaign_graph,operation_time,total_campaign,xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### inventory in the storage buffer
    storage_inventory_plot(true_storage_inventory_graph,operation_time,true_buffer_max,true_buffer_min,'True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    storage_inventory_plot(expected_storage_inventory_graph,operation_time,expected_buffer_max,expected_buffer_min,'Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    storage_inventory_plot(measured_storage_inventory_graph,operation_time,measured_buffer_max,measured_buffer_min,'Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### batch weight plots
    batch_weight_plot(true_weight_graph,operation_time,true_throughput,'True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    batch_weight_plot(expected_weight_graph,operation_time,expected_throughput,'Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    batch_weight_plot(measured_weight_graph,operation_time,measured_throughput,'Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### processed inventory plots
    processed_inventory_plot(true_processed_inventory_graph,operation_time,true_processed,'True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    processed_inventory_plot(expected_processed_inventory_graph,operation_time,expected_processed,'Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    processed_inventory_plot(measured_processed_inventory_graph,operation_time,measured_processed,'Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### MUF plots
    muf_plot(true_muf_graph,operation_time,true_muf,'True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    muf_plot(expected_muf_graph,operation_time,expected_muf,'Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    muf_plot(measured_muf_graph,operation_time,measured_muf,'Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### total melter failures
    total_melter_failure_plot(total_melter_failure_graph,total_campaign,total_melter_failure,1)
###
#
### system false alarms
    system_false_alarm_plot(system_false_alarm_counter_graph,total_campaign,system_false_alarm_counter,1)
    system_false_alarm_threshold_plot(system_false_alarm_threshold_graph,operation_time,system_false_alarm_threshold,xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### KMP measurements
    kmp_plot(true_kmp0_graph,operation_time,true_throughput,'0','True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(true_kmp1_graph,operation_time,true_throughput,'1','True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(true_kmp2_graph,operation_time,true_throughput,'2','True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(true_kmp3_graph,operation_time,true_throughput,'3','True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(true_kmp4_graph,operation_time,true_throughput,'4','True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
#
    kmp_plot(expected_kmp0_graph,operation_time,expected_throughput,'0','Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(expected_kmp1_graph,operation_time,expected_throughput,'1','Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(expected_kmp2_graph,operation_time,expected_throughput,'2','Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(expected_kmp3_graph,operation_time,expected_throughput,'3','Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(expected_kmp4_graph,operation_time,expected_throughput,'4','Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
#
    kmp_plot(measured_kmp0_graph,operation_time,measured_throughput,'0','Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(measured_kmp1_graph,operation_time,measured_throughput,'1','Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(measured_kmp2_graph,operation_time,measured_throughput,'2','Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(measured_kmp3_graph,operation_time,measured_throughput,'3','Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    kmp_plot(measured_kmp4_graph,operation_time,measured_throughput,'4','Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### Heel plots
# currently heel = MUF
# this will change when there is MUF in the trimmer
    heel_plot(true_heel_graph,operation_time,true_heel,'True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    heel_plot(expected_heel_graph,operation_time,expected_heel,'Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    heel_plot(measured_heel_graph,operation_time,measured_heel,'Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### system inventory transferred from buffer to melter
    system_inventory_plot(true_system_inventory_graph,operation_time,true_system,'True',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    system_inventory_plot(expected_system_inventory_graph,operation_time,expected_system,'Expected',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
    system_inventory_plot(measured_system_inventory_graph,operation_time,measured_system,'Measured',xmin_time,xmax_time,xmajortick_time,xminortick_time,1)
###
#
### return to home directory
    os.chdir(home_dir)
###
    return()
########################################################################
#
#
#
####### make the data files
def make_files_for_plot(home_dir,output_data_dir):
###
#
### change directory
    os.chdir(output_data_dir)
###
#
###
    total_campaign_graph=numpy.loadtxt('facility.campaign.out',dtype=float,delimiter='\t')
#
    true_storage_inventory_graph=numpy.loadtxt('true.storage.inventory.out',dtype=float,delimiter='\t')
    expected_storage_inventory_graph=numpy.loadtxt('expected.storage.inventory.out',dtype=float,delimiter='\t')
    measured_storage_inventory_graph=numpy.loadtxt('measured.storage.inventory.out',dtype=float,delimiter='\t')
#    
    true_weight_graph=numpy.loadtxt('true.weight.out',dtype=float,delimiter='\t')
    expected_weight_graph=numpy.loadtxt('expected.weight.out',dtype=float,delimiter='\t')
    measured_weight_graph=numpy.loadtxt('measured.weight.out',dtype=float,delimiter='\t')
#
    true_processed_inventory_graph=numpy.loadtxt('true.processed.inventory.out',dtype=float,delimiter='\t')
    expected_processed_inventory_graph=numpy.loadtxt('expected.processed.inventory.out',dtype=float,delimiter='\t')
    measured_processed_inventory_graph=numpy.loadtxt('measured.processed.inventory.out',dtype=float,delimiter='\t')
#
    true_muf_graph=numpy.loadtxt('true.muf.out',dtype=float,delimiter='\t')
    expected_muf_graph=numpy.loadtxt('expected.muf.out',dtype=float,delimiter='\t')
    measured_muf_graph=numpy.loadtxt('measured.muf.out',dtype=float,delimiter='\t')
#
    total_melter_failure_graph=numpy.loadtxt('total.melter.failures.out',dtype=float,delimiter='\t')
#
    system_false_alarm_counter_graph=numpy.loadtxt('system.false.alarm.counter.out',dtype=float,delimiter='\t')
    system_false_alarm_threshold_graph= numpy.loadtxt('system.false.alarm.threshold.out',dtype=float,delimiter='\t')
#
    true_kmp0_graph=numpy.loadtxt('true.kmp0.out',dtype=float,delimiter='\t')
    true_kmp1_graph=numpy.loadtxt('true.kmp1.out',dtype=float,delimiter='\t')
    true_kmp2_graph=numpy.loadtxt('true.kmp2.out',dtype=float,delimiter='\t')
    true_kmp3_graph=numpy.loadtxt('true.kmp3.out',dtype=float,delimiter='\t')
    true_kmp4_graph=numpy.loadtxt('true.kmp4.out',dtype=float,delimiter='\t')
#
    expected_kmp0_graph=numpy.loadtxt('expected.kmp0.out',dtype=float,delimiter='\t')
    expected_kmp1_graph=numpy.loadtxt('expected.kmp1.out',dtype=float,delimiter='\t')
    expected_kmp2_graph=numpy.loadtxt('expected.kmp2.out',dtype=float,delimiter='\t')
    expected_kmp3_graph=numpy.loadtxt('expected.kmp3.out',dtype=float,delimiter='\t')
    expected_kmp4_graph=numpy.loadtxt('expected.kmp4.out',dtype=float,delimiter='\t')
#
    measured_kmp0_graph=numpy.loadtxt('measured.kmp0.out',dtype=float,delimiter='\t')
    measured_kmp1_graph=numpy.loadtxt('measured.kmp1.out',dtype=float,delimiter='\t')
    measured_kmp2_graph=numpy.loadtxt('measured.kmp2.out',dtype=float,delimiter='\t')
    measured_kmp3_graph=numpy.loadtxt('measured.kmp3.out',dtype=float,delimiter='\t')
    measured_kmp4_graph=numpy.loadtxt('measured.kmp4.out',dtype=float,delimiter='\t')
#
    true_heel_graph=numpy.loadtxt('true.heel.out',dtype=float,delimiter='\t')
    expected_heel_graph=numpy.loadtxt('expected.heel.out',dtype=float,delimiter='\t')
    measured_heel_graph=numpy.loadtxt('measured.heel.out',dtype=float,delimiter='\t')
#
    true_system_inventory_graph=numpy.loadtxt('true.system.inventory.out',dtype=float,delimiter='\t')
    expected_system_inventory_graph=numpy.loadtxt('expected.system.inventory.out',dtype=float,delimiter='\t')
    measured_system_inventory_graph=numpy.loadtxt('measured.system.inventory.out',dtype=float,delimiter='\t')
###
#
### return to home dir
    os.chdir(home_dir)
###
    return(total_campaign_graph,true_storage_inventory_graph,expected_storage_inventory_graph,measured_storage_inventory_graph,true_weight_graph,expected_weight_graph,measured_weight_graph,true_processed_inventory_graph,expected_processed_inventory_graph,measured_processed_inventory_graph,true_muf_graph,expected_muf_graph,measured_muf_graph,total_melter_failure_graph,system_false_alarm_counter_graph,true_kmp0_graph,true_kmp1_graph,true_kmp2_graph,true_kmp3_graph,true_kmp4_graph,expected_kmp0_graph,expected_kmp1_graph,expected_kmp2_graph,expected_kmp3_graph,expected_kmp4_graph,measured_kmp0_graph,measured_kmp1_graph,measured_kmp2_graph,measured_kmp3_graph,measured_kmp4_graph,true_heel_graph,expected_heel_graph,measured_heel_graph,true_system_inventory_graph,expected_system_inventory_graph,measured_system_inventory_graph,system_false_alarm_threshold_graph)
########################################################################    
#
#
#
########################################################################
#
# individual plot functiono
#
########################################################################
#
#
#
####### completed campaign v facility operation
def campaign_plot(plotdata,operation_time,total_campaign,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title='Total campaigns processed'
    xtitle='Facility operation time (d)'
    ytitle='Campaigns processed'
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=0.50
    ymax=(total_campaign-1)+0.50
#
    xmajortick=xmajortick_time
    ymajortick=2
#
    xminortick=xminortick_time
    yminortick=1
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### storage inventory in the buffer v facility operation
def storage_inventory_plot(plotdata,operation_time,storage_buffer_max,storage_buffer_min,buffer_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1=buffer_type
    title2=' storage inventory in the buffer'
    ytitle1=buffer_type
    ytitle2=' unprocessed inventory (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=storage_buffer_min-9
    ymax=storage_buffer_max+9
#
    xmajortick=xmajortick_time
    ymajortick=50
#
    xminortick=xminortick_time
    yminortick=25
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### batch weight v facility operation
def batch_weight_plot(plotdata,operation_time,throughput,batch_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1=batch_type
    title2=' material throughput'
    ytitle1=batch_type
    ytitle2=' weight (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=-.50
    ymax=throughput+0.25
#
    xmajortick=xmajortick_time
    ymajortick=5
#
    xminortick=xminortick_time
    yminortick=1
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### processed inventory v facility operation
def processed_inventory_plot(plotdata,operation_time,processed_material,processed_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1=processed_type
    title2=' processed inventory'
    ytitle1=processed_type
    ytitle2=' processed inventory (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=-9
    ymax=processed_material+9
#
    xmajortick=xmajortick_time
    ymajortick=50
#
    xminortick=xminortick_time
    yminortick=25
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### muf v facility operation
def muf_plot(plotdata,operation_time,muf,muf_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1=muf_type
    title2=' material unaccounted for'
    ytitle1=muf_type
    ytitle2=' MUF (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=-0.10
    ymax=muf+0.10
#
    xmajortick=xmajortick_time
    ymajortick=0.25
#
    xminortick=xminortick_time
    yminortick=0.10
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### total melter failures v campaign
def total_melter_failure_plot(plotdata,total_campaign,total_melter_failure,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title='Total melter failures'
    xtitle='Campaigns processed'
    ytitle='Failure events'
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=0.50
    xmax=(total_campaign-1)+0.50
#
    ymin=-0.50
    ymax=(total_melter_failure+0.50)
#
    xmajortick=1
    ymajortick=1
#
#    xminortick=0
#    yminortick=0
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
#    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
#    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### total system false alarms v campaign
def system_false_alarm_plot(plotdata,total_campaign,system_false_alarm_counter,grid_parameter):
###
#
### This is for the false alarms trigger due to system inspection, not at KMPs
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title='System false alarms due to inspection'
    xtitle='Campaigns processed'
    ytitle='False alarms'
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=0.50
    xmax=(total_campaign-1)+0.50
#
    ymin=-0.50
    ymax=(system_false_alarm_counter+0.50)
#
    xmajortick=2
    ymajortick=2
#
    xminortick=1
    yminortick=1
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### kmp
def kmp_plot(plotdata,operation_time,throughput,kmp_identifier,kmp_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1='Record at KMP'
    title2=kmp_identifier
    ytitle1=kmp_type
    ytitle2=' weight (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=throughput-2.5
    ymax=throughput
#
    xmajortick=xmajortick_time
    ymajortick=.25
#
    xminortick=xminortick_time
    yminortick=0.10
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### heel v facility operation
# heel is the accumulated crucible measured at KMP3 when failure
###
def heel_plot(plotdata,operation_time,heel,heel_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1=heel_type
    title2=' heel'
    ytitle1=heel_type
    ytitle2=' heel (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=-0.10
    ymax=heel+0.15
#
    xmajortick=xmajortick_time
    ymajortick=0.25
#
    xminortick=xminortick_time
    yminortick=0.10
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### system inventory v facility operation
def system_inventory_plot(plotdata,operation_time,system,system_type,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title1=system_type
    title2=' transferred inventory'
    ytitle1=system_type
    ytitle2=' system inventory (kg)'
    title=title1+title2
    xtitle='Facility operation time (d)'
    ytitle=ytitle1+ytitle2
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=-4
    ymax=system+4
#
    xmajortick=xmajortick_time
    ymajortick=25
#
    xminortick=xminortick_time
    yminortick=10
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1])
    plot.get_current_fig_manager().resize(1024,800)    
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
#######
#
#
#
####### system thesholds v facility operation and user threshold
def system_false_alarm_threshold_plot(plotdata,operation_time,threshold,xmin_time,xmax_time,xmajortick_time,xminortick_time,grid_parameter):
###
#
# set up for two y axis
    fig,left_axis=plot.subplots()
#right_axis=left_axis.twinx()
###
# plot text
    title='System false alarm threshold tests'
    xtitle='Facility operation time (d)'
    ytitle='Threshold (kg)'
###
    plot.title(title)
    left_axis.set_xlabel(xtitle)
    left_axis.set_ylabel(ytitle)
#right_axis.set_ylabel()
###
# axis
    xmin=xmin_time
    xmax=xmax_time
#
    ymin=-0.03
    ymax=threshold+0.03
#
    xmajortick=xmajortick_time
    ymajortick=0.05
#
    xminortick=xminortick_time
    yminortick=0.025
###
    plot.xlim(xmin,xmax)
    left_axis.axis(ymin=ymin,ymax=ymax)
#
    left_axis.xaxis.set_major_locator(MultipleLocator(xmajortick))
    left_axis.xaxis.set_minor_locator(MultipleLocator(xminortick))
    left_axis.yaxis.set_major_locator(MultipleLocator(ymajortick))
    left_axis.yaxis.set_minor_locator(MultipleLocator(yminortick))
#
    left_axis.tick_params(axis='both',which='major',direction='inout',length=7)
###
# grid
    if grid_parameter==1:
        left_axis.grid(which='major',axis='both',linewidth='1.1')
#       left_axis.grid(which='minor',axis='both')
###
# plot
    left_axis.plot(plotdata[:,0],plotdata[:,1],plotdata[:,0],plotdata[:,2])
    plot.get_current_fig_manager().resize(1024,800)    
    plot.show()
###
#
### save
    plot.savefig(title)
###
    return()
########################################################################
#
#
#
########################################################################
#
# false alarm probability functions
#
########################################################################
#
#
#
####### system false alarm probability
### this is the function for the false alarm probability that is called in the main file
# the identifier designates whether it is for system or KMP false alarms
def false_alarm_probability(false_alarm_identifier,home_dir,output_data_dir):
###
#
### change directory
    os.chdir(output_data_dir)
###
#    
### set file name for loading and writing
    filename_base='.false.alarm.counter.out'
###
#
### load data
    false_alarm_threshold,time_steps=make_false_alarm_threshold(false_alarm_identifier,filename_base)
###
#
### initialize variables
    false_alarm_attempt=0
    false_alarm_trigger=0
    false_alarm_error=0
###
#
### tally up attempts and triggers 
    for i in range(0,time_steps):
	if (false_alarm_threshold[i,1]!=0):
	    false_alarm_attempt=false_alarm_attempt+1
	    if (false_alarm_threshold[i,1]>false_alarm_threshold[i,2]):
		false_alarm_trigger=false_alarm_trigger+1
# end if
# end if
# end j 
###
    false_alarm_error=float(false_alarm_trigger)/float(false_alarm_attempt)
###
#
### write false alarm error file
    threshold=false_alarm_threshold[0,2] # this is the threshold level that triggers the false alarm
    write_false_alarm_error_file(threshold,false_alarm_error,false_alarm_trigger,false_alarm_attempt,false_alarm_identifier)
###
#
### go to home directory
    os.chdir(home_dir)
###
    return()
####### 
#
#
#
######## construct alarm test v time for false alarm 
def make_false_alarm_threshold(false_alarm_identifier,filename_base):
###
#
### set up file name for system or kmp and open the file
    false_alarm_filename=false_alarm_identifier+filename_base
    false_alarm_counter=numpy.loadtxt(false_alarm_filename,dtype=float,delimiter='\t')
###
#
### get number of time steps, this includes t = 0
    time_steps=len(false_alarm_counter)
###
#
### initialize matrix
    false_alarm_threshold=numpy.zeros((time_steps,3))
###
#
### set time domain and threshold 
    for i in range(0,time_steps):
        false_alarm_threshold[i,0]=false_alarm_counter[i,4]
        false_alarm_threshold[i,2]=false_alarm_counter[i,2]
### end i
#
### first row alarm test = zero at t = 0
#
### the rest
    for j in range(1,time_steps):
        if (false_alarm_counter[j,3]>0) and (false_alarm_counter[j-1,3]==0):
            false_alarm_threshold[j,1]=false_alarm_counter[j,3]
        elif (false_alarm_counter[j,3]>0) and (false_alarm_counter[j,3]!=false_alarm_counter[j-1,3]):
            false_alarm_threshold[j,1]=false_alarm_counter[j,3]
### end if
#
### save file
    filename_base='.false.alarm.threshold.out'
    false_alarm_filename=false_alarm_identifier+filename_base
    numpy.savetxt(false_alarm_filename,false_alarm_threshold,fmt=['%.4f','%.4f','%.4f'],delimiter='\t')
###
    return(false_alarm_threshold,time_steps)
#######
#
#
#
####### write false alarm probability file
def write_false_alarm_error_file(threshold,false_alarm_error,false_alarm_trigger,false_alarm_attempt,false_alarm_identifier): 
###
#
### set up filename
    filename_base='.false.alarm.probability.out'
    false_alarm_filename=false_alarm_identifier+filename_base
###
#
### check to see if the file already exists or create if not
    if os.path.isfile(false_alarm_filename):
        print false_alarm_filename,' exists'
	false_alarm_file_output=open(false_alarm_filename,'a')
    else:
        print false_alarm_filename,' does not exist'
        false_alarm_file_output=open(false_alarm_filename,'w+')
### end if
    false_alarm_file_output.write(str.format('%.4f'%threshold)+'\t'+str.format('%.4f'%false_alarm_error)+'\t'+str.format('%.4f'%false_alarm_trigger)+'\t'+str.format('%.4f'%false_alarm_attempt)+'\n') 
###
#
### close file
    false_alarm_file_output.close()
###
    return()
########################################################################
#
#
#
########################################################################
#      EOF
########################################################################
