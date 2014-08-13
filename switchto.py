# -*- coding: utf-8 -*-
import sys
from workflow import Workflow, MATCH_STARTSWITH, MATCH_SUBSTRING, MATCH_ATOM
from subprocess import Popen, PIPE

def main(wf):

         #create and send applescript
         scpt0 = '''set theResults to {}
                    set theWindows to {}
                    tell application "System Events"
                        repeat with this_process in processes
                            if not background only of this_process then
                                tell this_process
                                    set the_app to name
                                    set theFile to the file of this_process
                                    set theWindows to name of windows
                                end tell
                                repeat with i from 1 to length of theWindows
                                    set theResults to theResults & "\n\n" & {theFile} & "\n" & {the_app} & "\n" & {(item i of theWindows)}
                                end repeat
                            end if
                        end repeat
                    end tell
                    return theResults'''

         p1 = Popen(['osascript',  '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
         prcs, stderr = p1.communicate(scpt0)

         #massage-decode and split into list
         prcs = (str(prcs)).decode('utf-8', errors='ignore').split('\n\n')

         prcs = prcs[1:]

         window_name = "" 
         process_name = ""
         icon = ""

         if len(wf.args):
             query = wf.args[0]
         else:
             query = None

         # filter windows with query
         if query:
            prcs = wf.filter(query, prcs, match_on=MATCH_STARTSWITH | MATCH_SUBSTRING | MATCH_ATOM)

         #divide components
         for prc in prcs:
               prc = prc.split('\n')
   
               try:
                 process_name = prc[1].strip(', ')
               except:
                 process_name = ""

               try:
                 window_name = prc[2].strip(', ')
               except:
                 window_name = ""

               try:
                   icon = prc[0].strip(', ')[18:][:-1].replace(':','/')
               except:
                   icon = "icon.png"


               wf.add_item(title=window_name,
                           subtitle="switch to " + window_name,
                           icon=icon,
                           icontype="fileicon",
                           valid=True,
                           arg=process_name+'\n'+window_name) #need sth better than this weird delimiter


         
         #Send the results to Alfred as XML
         wf.send_feedback()


     



if __name__ == u"__main__":
     wf = Workflow()
     sys.exit(wf.run(main))




