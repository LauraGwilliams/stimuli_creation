file_path = '/Users/lauragwilliams/Documents/experiments/re/experiment_setup/presentation/pres_files/'


for i in range(0,24):
    path = '/Users/lauragwilliams/Documents/experiments/re/experiment_setup/presentation/psuedo_rand_lists/pseudo_rand_list' + str(i) + '.txt'
    ds = load.txt.tsv(path, True, delimiter='\t', ignore_missing=True)
    
    presentation_code(rand=ds,cor_but='good_bad',file_path=file_path,n=i)


malarky_begn = """TEMPLATE "re_un_out_MainTrial.tem" {

word	Port_Code	correct_button	order	;"""

malarky_break1 = """};

text { caption = "Block 1 of 4 Complete.


Press any button to continue."; font_size = 30; } break1;

picture {
   background_color = 150,150,150;

   text break1;
   x = 0; y = 100;
 
} break_pic1;

trial {
   trial_type = first_response;
   trial_duration = forever;

   picture break_pic1;

};


trial {
    trial_duration = stimuli_length;
    trial_type = fixed;
		
picture {
        text asterisk;
        x = 0; y = 0;

    };

time = 0;    
duration = 1000;

};

TEMPLATE "re_un_out_MainTrial.tem" {
word	Port_Code	correct_button	order	;"""


malarky_break2 = """};

text { caption = "Block 2 of 4 Complete.


Press any button to continue."; font_size = 30; } break2;

picture {
   background_color = 150,150,150;

   text break2;
   x = 0; y = 100;
 
} break_pic2;

trial {
   trial_type = first_response;
   trial_duration = forever;

   picture break_pic2;

};


trial {
    trial_duration = stimuli_length;
    trial_type = fixed;
		
picture {
        text asterisk;
        x = 0; y = 0;

    };

time = 0;    
duration = 1000;

};

TEMPLATE "re_un_out_MainTrial.tem" {
word	Port_Code	correct_button	order	;"""


malarky_break3 = """
};

text { caption = "Block 3 of 4 Complete.


Press any button to continue."; font_size = 30; } break3;

picture {
   background_color = 150,150,150;

   text break3;
   x = 0; y = 100;
 
} break_pic3;

trial {
   trial_type = first_response;
   trial_duration = forever;

   picture break_pic3;

};


trial {
    trial_duration = stimuli_length;
    trial_type = fixed;
		
picture {
        text asterisk;
        x = 0; y = 0;

    };

time = 0;    
duration = 1000;

};

TEMPLATE "re_un_out_MainTrial.tem" {
word	Port_Code	correct_button	order	;
"""


end = """};



text { caption = "The experiment is now over. Thank you for your participation!

Please lay still while we save the recording."; font_size = 30; } theEnd_text;

picture {
   background_color = 150,150,150;

   text theEnd_text;
   x = 0; y = 100;
 
} theEnd_pic;


trial {
   trial_type = specific_response;
	terminator_button = 3;
   trial_duration = forever;

   picture theEnd_pic;

};"""



folder = '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/experiment/presentation/pseudo_rand_lists/'

for i in range(0,1):
    
    text_file = open("preslist%i.txt" %i, "w") # initiate the text file to be written
    
    path = folder + '/presentation_files' + str(i) + '.txt'
    ds = load.txt.tsv(path, True, delimiter='\t', ignore_missing=True)
    
    print "THIS IS LIST", i
    text_file.write("THIS IS LIST %i\n" %i)
    text_file.write(malarky_begn + '\n')
    for line in range(0,len(ds['word'])):
        keys = ds.keys()
        
        item_lines = ([ds[keys[0]][line], ds[keys[1]][line], ds[keys[2]][line], ds[keys[3]][line], ds[keys[4]][line]])
        item_lines = str(item_lines)
        
        chars_to_remove = [']','[','"'] # get rid of these characters when printing
        
        item_lines = item_lines.translate(None, ''.join(chars_to_remove))
        
        text_file.write(item_lines + '\n')
        
        if line == 132:
            print malarky_break1
            text_file.write(malarky_break1+ '\n')
        if line == 264:
            print malarky_break2
            text_file.write(malarky_break2+ '\n')
        if line == 396:
            print malarky_break3
            text_file.write(malarky_break3+ '\n')
        if line == 529:
            print end
            text_file.write(end+ '\n')   

            text_file.close() # once file complete, close to write the new one