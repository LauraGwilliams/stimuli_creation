#!/usr/bin/env python


from __future__ import division

from eelbrain import *
import numpy as np


sce = '''

# re_un_out Scenario File #

scenario = "VW";
no_logfile = false;
default_font_size = 32;
response_matching = simple_matching;
active_buttons = 3;
button_codes = 0, 0, 0;
default_background_color = 150,150,150;
default_font = "Arial";

# send codes to Meglab
write_codes = true;
pulse_width = 5;

begin;

# set up the instructions and information to be provided to subject #

text { caption = "Welcome to our experiment!

Please lay still while we set up the recording."; font_size = 30; } welcome_text;

picture {
   background_color = 150,150,150;

   text welcome_text;
   x = 0; y = 100;
 
} welcome_pic;


trial {
   trial_type = specific_response;
	terminator_button = 3;
   trial_duration = forever;

   picture welcome_pic;

};



text { caption = 

"When you see a word of English that you recognise, press the right button.
If you do not recognise the item, press the left button."; font_size = 30; } instruct1;

picture {
   background_color = 150,150,150;

   text instruct1;
   x = 0; y = 100;
 
} instruct1_pic;


text { caption = 

"First we will begin with a practice. Press either button to begin."; font_size = 30; } prac;

picture {
   background_color = 150,150,150;

   text prac;
   x = 0; y = 100;
 
} prac_pic;


trial {
   trial_type = first_response;
   trial_duration = forever;

   picture prac_pic;

};



# this is a break now! #

text { caption = 

"This is a break. Press any button when you are ready to continue."; font_size = 30; } break;

picture {
   background_color = 150,150,150;

   text break;
   x = 0; y = 100;
 
} break_pic;



# set up the fixation cross and word/non-word question #

text { caption = "+"; font_size = 50; font_color = 0,0,0; background_color = 150,150,150; } asterisk;
text { caption = "+"; font_size = 50; font_color = 255,0,0; background_color = 150,150,150; } asterisk_red;
text { caption = "?"; font_size = 40; } question;

# load practice trials
text { caption = "recannibalize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recannibalize;
text { caption = "unlawful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlawful;
text { caption = "outsuave"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outsuave;
text { caption = "outmoist"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmoist;
text { caption = "restraight"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }restraight;
text { caption = "outgun"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outgun;
text { caption = "ungypsy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungypsy;
text { caption = "unfaithful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfaithful;
text { caption = "outraced"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outraced;
text { caption = "repay"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }repay;
text { caption = "restiffen"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }restiffen;
text { caption = "outdifficult"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdifficult;
text { caption = "unpesto"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpesto;
text { caption = "reharsh"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reharsh;



# set up experiment stimuli #


text { caption = "retelling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retelling;
text { caption = "uneatable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uneatable;
text { caption = "unbalancing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbalancing;
text { caption = "outhappy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outhappy;
text { caption = "unpeat"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpeat;
text { caption = "unsticking"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsticking;
text { caption = "reidolize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reidolize;
text { caption = "unusable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unusable;
text { caption = "unbolted"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbolted;
text { caption = "redrawn"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redrawn;
text { caption = "rememorize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rememorize;
text { caption = "regenuine"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regenuine;
text { caption = "unstop"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unstop;
text { caption = "unblocked"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unblocked;
text { caption = "reitem"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reitem;
text { caption = "resemble"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resemble;
text { caption = "realigned"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }realigned;
text { caption = "recrystal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recrystal;
text { caption = "unlogic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlogic;
text { caption = "unseated"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unseated;
text { caption = "unflirt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unflirt;
text { caption = "reentered"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reentered;
text { caption = "unhitching"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhitching;
text { caption = "outpace"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outpace;
text { caption = "recriticize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recriticize;
text { caption = "rewashed"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rewashed;
text { caption = "unsniffed"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsniffed;
text { caption = "ungirlish"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungirlish;
text { caption = "reenacted"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reenacted;
text { caption = "unbucked"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbucked;
text { caption = "unclingy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unclingy;
text { caption = "unplugged"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unplugged;
text { caption = "outshine"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outshine;
text { caption = "outblue"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outblue;
text { caption = "unstitched"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unstitched;
text { caption = "outhoarse"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outhoarse;
text { caption = "uncovering"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncovering;
text { caption = "relearnt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relearnt;
text { caption = "recoarse"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recoarse;
text { caption = "redumb"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redumb;
text { caption = "unchained"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unchained;
text { caption = "outaloof"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outaloof;
text { caption = "refraught"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refraught;
text { caption = "ungawking"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungawking;
text { caption = "reholler"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reholler;
text { caption = "refertile"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refertile;
text { caption = "unpraying"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpraying;
text { caption = "regurgle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regurgle;
text { caption = "replenish"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }replenish;
text { caption = "reattached"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reattached;
text { caption = "outdrive"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdrive;
text { caption = "outmuzzle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmuzzle;
text { caption = "remodernize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remodernize;
text { caption = "ungoat"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungoat;
text { caption = "outremind"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outremind;
text { caption = "ungrumbling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungrumbling;
text { caption = "outrich"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outrich;
text { caption = "outdizzy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdizzy;
text { caption = "uncrossed"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncrossed;
text { caption = "rewide"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rewide;
text { caption = "outmurder"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmurder;
text { caption = "reassigning"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reassigning;
text { caption = "unsheathed"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsheathed;
text { caption = "outawkward"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outawkward;
text { caption = "rehired"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rehired;
text { caption = "remedy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remedy;
text { caption = "unfleshy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfleshy;
text { caption = "uncoiling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncoiling;
text { caption = "relay"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relay;
text { caption = "rearrange"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rearrange;
text { caption = "remaking"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remaking;
text { caption = "regentle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regentle;
text { caption = "relegalize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relegalize;
text { caption = "recheap"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recheap;
text { caption = "reneaten"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reneaten;
text { caption = "regrown"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regrown;
text { caption = "outfish"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outfish;
text { caption = "unwork"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwork;
text { caption = "unfastened"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfastened;
text { caption = "unfoot"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfoot;
text { caption = "uncabin"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncabin;
text { caption = "unyelling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unyelling;
text { caption = "repopularize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }repopularize;
text { caption = "unlatching"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlatching;
text { caption = "unsealing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsealing;
text { caption = "unnotice"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unnotice;
text { caption = "relocate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relocate;
text { caption = "restable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }restable;
text { caption = "outargue"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outargue;
text { caption = "rebrutal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebrutal;
text { caption = "reconcile"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reconcile;
text { caption = "reselling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reselling;
text { caption = "untrot"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untrot;
text { caption = "unglobe"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglobe;
text { caption = "reenter"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reenter;
text { caption = "rewrapped"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rewrapped;
text { caption = "relaugh"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relaugh;
text { caption = "unfinished"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfinished;
text { caption = "redemonize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redemonize;
text { caption = "unfruit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfruit;
text { caption = "uncamel"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncamel;
text { caption = "unbody"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbody;
text { caption = "unbeast"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbeast;
text { caption = "ungnome"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungnome;
text { caption = "unfaith"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfaith;
text { caption = "unhairy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhairy;
text { caption = "rechirp"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rechirp;
text { caption = "recite"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recite;
text { caption = "reinventing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reinventing;
text { caption = "unblow"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unblow;
text { caption = "unthink"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unthink;
text { caption = "outfight"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outfight;
text { caption = "uncoffee"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncoffee;
text { caption = "readjust"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }readjust;
text { caption = "ungraceful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungraceful;
text { caption = "outspend"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outspend;
text { caption = "reusing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reusing;
text { caption = "unpack"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpack;
text { caption = "uneagle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uneagle;
text { caption = "unprepare"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unprepare;
text { caption = "unwashing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwashing;
text { caption = "unbible"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbible;
text { caption = "unoccupy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unoccupy;
text { caption = "repray"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }repray;
text { caption = "rehonest"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rehonest;
text { caption = "unglassy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglassy;
text { caption = "unimagine"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unimagine;
text { caption = "resnivel"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resnivel;
text { caption = "unwife"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwife;
text { caption = "outeerie"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outeerie;
text { caption = "reassure"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reassure;
text { caption = "reacquired"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reacquired;
text { caption = "unlimb"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlimb;
text { caption = "unhook"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhook;
text { caption = "unboasting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unboasting;
text { caption = "outmuffle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmuffle;
text { caption = "unmyth"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmyth;
text { caption = "ungape"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungape;
text { caption = "unweek"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unweek;
text { caption = "unfungi"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfungi;
text { caption = "reheight"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reheight;
text { caption = "reacquire"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reacquire;
text { caption = "outcivic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outcivic;
text { caption = "unapple"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unapple;
text { caption = "reyawn"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reyawn;
text { caption = "unlovable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlovable;
text { caption = "resoften"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resoften;
text { caption = "regladden"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regladden;
text { caption = "reckon"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reckon;
text { caption = "unfate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfate;
text { caption = "outamend"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outamend;
text { caption = "outinform"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outinform;
text { caption = "refierce"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refierce;
text { caption = "outkeep"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outkeep;
text { caption = "resending"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resending;
text { caption = "unfame"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfame;
text { caption = "revolve"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }revolve;
text { caption = "undigital"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undigital;
text { caption = "unlamp"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlamp;
text { caption = "outstrip"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outstrip;
text { caption = "uncloaked"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncloaked;
text { caption = "undruidic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undruidic;
text { caption = "unpouting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpouting;
text { caption = "outsource"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outsource;
text { caption = "outgain"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outgain;
text { caption = "unfasten"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfasten;
text { caption = "retitter"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retitter;
text { caption = "rebrisk"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebrisk;
text { caption = "uncork"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncork;
text { caption = "resettle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resettle;
text { caption = "unscrambling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unscrambling;
text { caption = "unjaunty"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unjaunty;
text { caption = "unbalance"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbalance;
text { caption = "unsorrow"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsorrow;
text { caption = "retrying"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retrying;
text { caption = "rememory"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rememory;
text { caption = "unmeal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmeal;
text { caption = "reionize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reionize;
text { caption = "reclever"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reclever;
text { caption = "unseat"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unseat;
text { caption = "remelted"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remelted;
text { caption = "outact"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outact;
text { caption = "resniff"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resniff;
text { caption = "outhot"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outhot;
text { caption = "reideal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reideal;
text { caption = "outprim"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outprim;
text { caption = "untact"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untact;
text { caption = "outlarge"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outlarge;
text { caption = "recruit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recruit;
text { caption = "relength"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relength;
text { caption = "unlock"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlock;
text { caption = "redeaf"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redeaf;
text { caption = "unlacing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlacing;
text { caption = "reject"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reject;
text { caption = "outrival"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outrival;
text { caption = "redramatize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redramatize;
text { caption = "reworsen"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reworsen;
text { caption = "retough"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retough;
text { caption = "reterror"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reterror;
text { caption = "unfable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfable;
text { caption = "outearn"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outearn;
text { caption = "outclass"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outclass;
text { caption = "unlace"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlace;
text { caption = "outentire"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outentire;
text { caption = "unstick"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unstick;
text { caption = "outarouse"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outarouse;
text { caption = "unbicker"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbicker;
text { caption = "regulate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regulate;
text { caption = "outlegal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outlegal;
text { caption = "unjoyful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unjoyful;
text { caption = "revocal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }revocal;
text { caption = "refute"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refute;
text { caption = "unclasping"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unclasping;
text { caption = "unwritten"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwritten;
text { caption = "reflounce"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reflounce;
text { caption = "relived"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relived;
text { caption = "regalore"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regalore;
text { caption = "untire"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untire;
text { caption = "refinalize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refinalize;
text { caption = "realphabet"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }realphabet;
text { caption = "unblock"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unblock;
text { caption = "unflesh"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unflesh;
text { caption = "unglass"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglass;
text { caption = "resqueal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resqueal;
text { caption = "unshave"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unshave;
text { caption = "uncomplaining"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncomplaining;
text { caption = "relocalize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relocalize;
text { caption = "unfibre"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfibre;
text { caption = "regrumble"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regrumble;
text { caption = "rebleak"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebleak;
text { caption = "outirate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outirate;
text { caption = "unhoney"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhoney;
text { caption = "outgive"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outgive;
text { caption = "outsmart"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outsmart;
text { caption = "reprieve"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reprieve;
text { caption = "reinstalled"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reinstalled;
text { caption = "oututter"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }oututter;
text { caption = "untrust"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untrust;
text { caption = "uncompete"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncompete;
text { caption = "recroak"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recroak;
text { caption = "unscrew"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unscrew;
text { caption = "unbabyish"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbabyish;
text { caption = "unhelpful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhelpful;
text { caption = "unboy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unboy;
text { caption = "refickle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refickle;
text { caption = "receive"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }receive;
text { caption = "realign"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }realign;
text { caption = "recommitting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recommitting;
text { caption = "retrieve"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retrieve;
text { caption = "outfamous"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outfamous;
text { caption = "unmealy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmealy;
text { caption = "redoze"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redoze;
text { caption = "redual"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redual;
text { caption = "unidiom"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unidiom;
text { caption = "unskillful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unskillful;
text { caption = "reapologize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reapologize;
text { caption = "rewhirr"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rewhirr;
text { caption = "reweaken"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reweaken;
text { caption = "unglueing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglueing;
text { caption = "unbeer"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbeer;
text { caption = "unglandular"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglandular;
text { caption = "unfateful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfateful;
text { caption = "rebroaden"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebroaden;
text { caption = "ungawk"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungawk;
text { caption = "remagnetize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remagnetize;
text { caption = "undock"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undock;
text { caption = "outsolve"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outsolve;
text { caption = "remarry"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remarry;
text { caption = "unlady"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlady;
text { caption = "ungrinded"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungrinded;
text { caption = "unodor"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unodor;
text { caption = "outbizarre"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outbizarre;
text { caption = "retoddle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retoddle;
text { caption = "outajar"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outajar;
text { caption = "unhitch"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhitch;
text { caption = "unrabbit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unrabbit;
text { caption = "recommit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recommit;
text { caption = "outpoor"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outpoor;
text { caption = "unduvet"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unduvet;
text { caption = "outprovoke"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outprovoke;
text { caption = "reapt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reapt;
text { caption = "recute"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recute;
text { caption = "unidiotic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unidiotic;
text { caption = "outcancel"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outcancel;
text { caption = "untame"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untame;
text { caption = "outdraw"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdraw;
text { caption = "uncover"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncover;
text { caption = "refill"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refill;
text { caption = "outabsurd"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outabsurd;
text { caption = "outhold"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outhold;
text { caption = "reflect"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reflect;
text { caption = "outspot"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outspot;
text { caption = "redeaden"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redeaden;
text { caption = "unkite"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unkite;
text { caption = "unjump"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unjump;
text { caption = "rebright"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebright;
text { caption = "unbend"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbend;
text { caption = "ungrape"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungrape;
text { caption = "redevout"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redevout;
text { caption = "untucked"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untucked;
text { caption = "uncar"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncar;
text { caption = "unfabled"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfabled;
text { caption = "repenal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }repenal;
text { caption = "outslay"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outslay;
text { caption = "unaunt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unaunt;
text { caption = "outtell"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outtell;
text { caption = "retain"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retain;
text { caption = "unfocused"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfocused;
text { caption = "outdodge"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdodge;
text { caption = "outspurn"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outspurn;
text { caption = "unthank"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unthank;
text { caption = "outgross"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outgross;
text { caption = "regiggle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }regiggle;
text { caption = "reeager"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reeager;
text { caption = "unclog"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unclog;
text { caption = "unmove"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmove;
text { caption = "unchasm"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unchasm;
text { caption = "reelecting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reelecting;
text { caption = "unbiblical"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbiblical;
text { caption = "unclasp"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unclasp;
text { caption = "outmake"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmake;
text { caption = "reeconomy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reeconomy;
text { caption = "rechortle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rechortle;
text { caption = "outflank"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outflank;
text { caption = "unchain"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unchain;
text { caption = "reample"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reample;
text { caption = "uncheerful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncheerful;
text { caption = "resocialize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resocialize;
text { caption = "resubmitted"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resubmitted;
text { caption = "uncouth"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncouth;
text { caption = "resleep"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resleep;
text { caption = "reable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reable;
text { caption = "unroll"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unroll;
text { caption = "rehowl"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rehowl;
text { caption = "recentral"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recentral;
text { caption = "unbeach"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbeach;
text { caption = "redense"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redense;
text { caption = "resick"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resick;
text { caption = "unrobotic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unrobotic;
text { caption = "outrude"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outrude;
text { caption = "refeeble"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refeeble;
text { caption = "resweeten"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resweeten;
text { caption = "reassign"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reassign;
text { caption = "unpath"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpath;
text { caption = "outglad"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outglad;
text { caption = "outcruel"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outcruel;
text { caption = "unplug"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unplug;
text { caption = "outdrink"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdrink;
text { caption = "reenact"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reenact;
text { caption = "outbad"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outbad;
text { caption = "rebuke"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebuke;
text { caption = "remagnet"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }remagnet;
text { caption = "unstitch"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unstitch;
text { caption = "outdare"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdare;
text { caption = "recreate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recreate;
text { caption = "recollect"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recollect;
text { caption = "unprove"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unprove;
text { caption = "unmeat"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmeat;
text { caption = "uneat"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uneat;
text { caption = "unthawed"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unthawed;
text { caption = "redeem"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redeem;
text { caption = "reformal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reformal;
text { caption = "refatten"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refatten;
text { caption = "relearn"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relearn;
text { caption = "recapital"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recapital;
text { caption = "reappear"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reappear;
text { caption = "ungland"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungland;
text { caption = "untwisting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untwisting;
text { caption = "outveto"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outveto;
text { caption = "resist"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resist;
text { caption = "unsneezing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsneezing;
text { caption = "outneat"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outneat;
text { caption = "rehuff"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rehuff;
text { caption = "unflavorful"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unflavorful;
text { caption = "unhealth"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhealth;
text { caption = "rescue"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rescue;
text { caption = "resputter"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resputter;
text { caption = "ungrow"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungrow;
text { caption = "unaccept"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unaccept;
text { caption = "outlast"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outlast;
text { caption = "outlax"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outlax;
text { caption = "reforeign"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reforeign;
text { caption = "unhair"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhair;
text { caption = "unpoem"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unpoem;
text { caption = "unbolt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbolt;
text { caption = "uncross"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncross;
text { caption = "outstare"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outstare;
text { caption = "unspit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unspit;
text { caption = "outbid"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outbid;
text { caption = "unwear"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwear;
text { caption = "unmelt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmelt;
text { caption = "unswitch"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unswitch;
text { caption = "retaken"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retaken;
text { caption = "reenergy"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reenergy;
text { caption = "retaliate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }retaliate;
text { caption = "outfresh"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outfresh;
text { caption = "outkill"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outkill;
text { caption = "unleash"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unleash;
text { caption = "unflatter"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unflatter;
text { caption = "unhabit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhabit;
text { caption = "unwandering"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwandering;
text { caption = "unatom"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unatom;
text { caption = "reasserting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reasserting;
text { caption = "resadden"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resadden;
text { caption = "unhour"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhour;
text { caption = "undo"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undo;
text { caption = "recasual"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recasual;
text { caption = "unfauna"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfauna;
text { caption = "outmaneuver"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmaneuver;
text { caption = "outweigh"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outweigh;
text { caption = "rejoice"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rejoice;
text { caption = "refold"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refold;
text { caption = "unshout"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unshout;
text { caption = "recustom"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recustom;
text { caption = "outcause"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outcause;
text { caption = "ungovern"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungovern;
text { caption = "reaffirm"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reaffirm;
text { caption = "untangle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untangle;
text { caption = "outmodern"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outmodern;
text { caption = "outdance"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outdance;
text { caption = "outignore"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outignore;
text { caption = "outhave"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outhave;
text { caption = "undress"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undress;
text { caption = "outglow"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outglow;
text { caption = "unatomic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unatomic;
text { caption = "unguest"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unguest;
text { caption = "rearid"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rearid;
text { caption = "untieing"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untieing;
text { caption = "unsuccess"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsuccess;
text { caption = "uncloak"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncloak;
text { caption = "rehire"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rehire;
text { caption = "unbutton"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbutton;
text { caption = "reshiver"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reshiver;
text { caption = "reinvent"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reinvent;
text { caption = "ungirl"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungirl;
text { caption = "rereading"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rereading;
text { caption = "unswimmable"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unswimmable;
text { caption = "recheep"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recheep;
text { caption = "rebald"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebald;
text { caption = "outfox"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outfox;
text { caption = "repudiate"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }repudiate;
text { caption = "uncurled"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncurled;
text { caption = "unmended"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmended;
text { caption = "repivot"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }repivot;
text { caption = "refrugal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refrugal;
text { caption = "readept"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }readept;
text { caption = "outusurp"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outusurp;
text { caption = "recomplain"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recomplain;
text { caption = "rechaste"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rechaste;
text { caption = "rebrittle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebrittle;
text { caption = "reacute"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reacute;
text { caption = "outbogus"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outbogus;
text { caption = "unidiot"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unidiot;
text { caption = "unfruity"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfruity;
text { caption = "outadvise"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outadvise;
text { caption = "reactual"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reactual;
text { caption = "untilting"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }untilting;
text { caption = "unload"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unload;
text { caption = "unspeak"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unspeak;
text { caption = "outlynch"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outlynch;
text { caption = "outnumber"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outnumber;
text { caption = "refrown"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refrown;
text { caption = "refrain"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }refrain;
text { caption = "reelect"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reelect;
text { caption = "unhotel"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhotel;
text { caption = "outnourish"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outnourish;
text { caption = "unhero"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unhero;
text { caption = "unmenu"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unmenu;
text { caption = "requicken"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }requicken;
text { caption = "outglum"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outglum;
text { caption = "uncider"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncider;
text { caption = "resplurge"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resplurge;
text { caption = "unlatch"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unlatch;
text { caption = "outperform"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outperform;
text { caption = "unboyish"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unboyish;
text { caption = "unjoined"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unjoined;
text { caption = "outstifle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outstifle;
text { caption = "unglue"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglue;
text { caption = "relive"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }relive;
text { caption = "outbuck"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outbuck;
text { caption = "outabrupt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outabrupt;
text { caption = "rebuild"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebuild;
text { caption = "unwailed"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwailed;
text { caption = "reassert"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reassert;
text { caption = "unbathe"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbathe;
text { caption = "redigit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redigit;
text { caption = "unwrinkling"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwrinkling;
text { caption = "unwalked"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unwalked;
text { caption = "rehumanize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rehumanize;
text { caption = "unglobal"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unglobal;
text { caption = "reattach"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reattach;
text { caption = "unsaddle"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unsaddle;
text { caption = "resubmit"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }resubmit;
text { caption = "undramatic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undramatic;
text { caption = "unbaby"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbaby;
text { caption = "revital"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }revital;
text { caption = "redie"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }redie;
text { caption = "rebawl"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }rebawl;
text { caption = "unbeastly"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unbeastly;
text { caption = "outshape"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }outshape;
text { caption = "recivil"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recivil;
text { caption = "undebt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undebt;
text { caption = "reripen"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reripen;
text { caption = "unheroic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unheroic;
text { caption = "revictimize"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }revictimize;
text { caption = "unfjord"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfjord;
text { caption = "recritic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }recritic;
text { caption = "reinstall"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reinstall;
text { caption = "unfood"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfood;
text { caption = "undemonic"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undemonic;
text { caption = "uncoil"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncoil;
text { caption = "uncurl"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }uncurl;
text { caption = "unaloe"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unaloe;
text { caption = "undiffer"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undiffer;
text { caption = "undruid"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }undruid;
text { caption = "ungalloped"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }ungalloped;
text { caption = "unjaunt"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unjaunt;
text { caption = "unfibrous"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }unfibrous;
text { caption = "renimble"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }renimble;
text { caption = "reyell"; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }reyell;

# feedback trial - show a red fixation for 1 sec if they get it wrong.

trial {
	  trial_duration = 500;
	  stimulus_event {
picture {
		  text asterisk_red;
		
		  x = 0; y = 0;
	};
};

}wrong_feedback;


TEMPLATE "re_un_out_Prac.tem" {
word	correct_button	;
unpesto	1	;
outsuave	1	;
outgun	2	;
repay	2	;
restiffen	1	;
outdifficult	1	;
reharsh	1	;
unlawful	2	;

};


text { caption = 

"
Practice over.

Please wait while we set up the recording."; font_size = 30; } begin1;

picture {
   background_color = 150,150,150;

   text begin1;
   x = 0; y = 100;
 
} begin_pic;

trial {
   trial_type = specific_response;
	terminator_button = 3;
   trial_duration = forever;

   picture begin_pic;

};

text { caption = 

"
Experiment ready.

Press any button to begin."; font_size = 30; } begin2;

picture {
   background_color = 150,150,150;

   text begin2;
   x = 0; y = 100;
 
} begin_pic2;

trial {
   trial_type = first_response;
   trial_duration = forever;

   picture begin_pic2;

};



'''

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

def text_obj_setup_presentation(row):
    """
    
    row         :           the column in your dataset to get the presentation output for
    
    """
    
    lines = []
    
    for item in row:
        lines.append( "text { caption = '" + item + "'; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }" + item + ";")
    
    ds = Dataset()
    ds['lines'] = Factor(lines)
    
    return ds
    
def presentation_code(rand,cor_but,diff_column,file_path,n=None):
    """
    
    rand            :           random presentation list
    cor_but         :           the column that has the thing that determines correct button
    file_path       :           where to save the lists
    n               :           list number to append to file
    
    """
    
    
    buttons = []
    
    # for status in rand[cor_but]:
    #     if status == 'bad':
    #         buttons.append(1)
    #     elif status == 'good':
    #         buttons.append(2)
    
    ds_temp = Dataset()
    items = rand[diff_column]
    Port_Code = rand['trigger']
    s = ";"
    ds_temp['item'] = Factor(items)
    ds_temp['Port_Code'] = Var(Port_Code)
    # ds_temp['correct_button'] = Var(buttons)
    ds_temp['order'] = rand['order']
    ds_temp['s'] = Factor(s*len(ds_temp['word']))

    ds_temp.save_txt(file_path + 'presentation_files' + str(n))
    
    
def scenario_list_pres(path_to_folder,number_of_items,save_dest,break_freq):
    """
    path_to_folder          :              where your rand lists are, up to the filename (e.g., file_path + '/presentation_files')".
                                           It will add the number and the .txt part)
    number_of_items         :              number of scenario files to create
    save_dest               :              where to save the files
    break_freq              :              how many breaks
    
    """
    
    for i in range(0,number_of_items):
    
        text_file = open(save_dest + "preslist%i.txt" %i, "w") # initiate the text file to be written

        path = path_to_folder + str(i) + '.txt'
        ds = load.txt.tsv(path, True, delimiter='\t', ignore_missing=True)
        
        length = len(ds[ds.keys()[0]])

        text_file.write("## THIS IS LIST %i\n" %i)
        text_file.write(sce + '\n')
        text_file.write(malarky_begn + '\n')
        for line in range(0,len(ds['word'])):
            keys = ds.keys()
        
            item_lines = ([ds[keys[0]][line], ds[keys[1]][line], ds[keys[2]][line], ds[keys[3]][line], ds[keys[4]][line]])
            item_lines = str(item_lines)
        
            chars_to_remove = [']','[','"',','] # get rid of these characters when printing
        
            item_lines = item_lines.translate(None, ''.join(chars_to_remove))
        
            text_file.write(item_lines + '\n')

            if line == (length/4)*1:
                text_file.write(malarky_break1+ '\n')
            if line == (length/4)*2:
                text_file.write(malarky_break2+ '\n')
            if line == (length/4)*3:
                text_file.write(malarky_break3+ '\n')
            if line+1 == length:
                text_file.write(end+ '\n')


        text_file.close() # once file complete, close to write the new one