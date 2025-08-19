#!/bin/tcsh

if ( $#argv == 0 ) then
   set fn = /dev/stdout
else
   set fn = $argv[1]
   /bin/rm -f $fn
endif
 
python --version


foreach f (TestUserModel.py)
  echo "###################################################" >> $fn
  echo "######## $f ##########################" >> $fn
  echo "###################################################" >> $fn
  echo "" >> $fn
  time python -m unittest $f:s/.py// >>& $fn
end


