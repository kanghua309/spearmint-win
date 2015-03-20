import os
import shutil
import signal
import sys
import pickle
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Locker
import ExperimentGrid
import subprocess

def reset():
  # Kill running workers.
  if os.path.exists('expt-grid.pkl'):
    try:
      locker = Locker.Locker()
      locker.lock(os.path.join(os.path.realpath('.'), 'expt-grid.pkllock'))
      with open('expt-grid.pkl', 'r') as f:
        expt_grid = pickle.load(f)
      for proc_ind in xrange(expt_grid['sgeids'].shape[0]):
        if expt_grid['status'][proc_ind] == ExperimentGrid.RUNNING_STATE:
          print 'Killing process with id: %s' % expt_grid['sgeids'][proc_ind]
          try:
            subprocess.check_call('taskkill /PID %s /F /T' % expt_grid['sgeids'][proc_ind])
          except:
            print 'Couldnt kill process with id: %s' % expt_grid['sgeids'][proc_ind]
    except Exception as e:
      print 'Couldnt clean up processes: %s.' % e.message
  # Clean up.
  # Jobs.
  if os.path.exists('jobs'):
    try:
      shutil.rmtree('jobs')
    except:
      print 'Couldnt remove jobs folder'
  # Outputs.
  if os.path.exists('output'):
    try:
      shutil.rmtree('output')
    except:
      try:
        time.sleep(5)
        shutil.rmtree('output')
      except:
        print 'Couldnt remove output folder'
  # Best result.
  if os.path.exists('best_job_and_result.txt'):
    try:
      os.remove('best_job_and_result.txt')
    except:
      print 'Couldnt remove best job file'
  # Experiment grid.
  if os.path.exists("expt-grid.pkl"):
    try:
      os.remove('expt-grid.pkl')
    except:
      print 'Couldnt remove experiment grid.'
  # GPEIOptChooser files.
  if os.path.exists('GPEIOptChooser.pkl'):
    try:
      os.remove('GPEIOptChooser.pkl')
      os.remove('GPEIOptChooser_hyperparameters.txt')
    except:
      print 'Couldnt remove GPEIOptChooser files.'
  # Trace.
  if os.path.exists('trace.csv'):
    try:
      os.remove('trace.csv')
    except:
      print 'Couldnt remove jobs folder'

