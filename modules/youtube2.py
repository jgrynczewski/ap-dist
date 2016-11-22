#!/bin/env python2.7
# -*- coding: utf-8 -*-

# This file is part of AP - Assistive Prototypes.
#
# AP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AP. If not, see <http://www.gnu.org/licenses/>.

import wxversion
# wxversion.select( '2.8' )

import Tkinter
import glob, os, time, sys, psutil

import wx
import wx.lib.buttons as bt

from pymouse import PyMouse
from string import maketrans
from pygame import mixer

from pilots import minitubePilot

#=============================================================================
class youtube2( wx.Frame ):
	def __init__(self, parent, id, con = 1):

		self.winWidth, self.winHeight = wx.DisplaySize( )
		wx.Frame.__init__( self , parent , id , 'AP Speller' )
		style = self.GetWindowStyle( )
		
		self.con = con
		
		if self.con !=0 :
			self.SetWindowStyle( style | wx.STAY_ON_TOP )
			self.parent = parent
		
			self.Maximize( True )
			self.Centre( True )
			self.MakeModal( True )
			
			self.initializeParameters( )
			self.initializeBitmaps( )
			self.createGui( )
			self.createBindings( )

			self.initializeTimer( )

		else:
			self.initializeParameters( )

	#-------------------------------------------------------------------------
	def initializeParameters(self):
                
		with open( './.pathToAP' ,'r' ) as textFile:
			self.pathToAP = textFile.readline( )
			
		sys.path.append( self.pathToAP )
		from reader import reader

		reader = reader()
		reader.readParameters()
		parameters = reader.getParameters()

		for item in parameters:
			try:
				setattr(self, item[:item.find('=')], int(item[item.find('=')+1:]))
			except ValueError:
				setattr(self, item[:item.find('=')], item[item.find('=')+1:])					    

		self.labels1 = [ 'A B C D E F G H I J K L M N O P R S T U W Y Z SPECIAL_CHARACTERS UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ) ]
		    
		self.labels2 = [ 'A O N S Y P J G I Z W C D U B F E R T K M L H SPECIAL_CHARACTERS UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ) ]

		self.labels3 = [ 'A O Z R T D J G I U N S K M B F E Y W C P L H SPECIAL_CHARACTERS UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ) ]

		self.labels4 = [ 'A E B C D F G H I O J K L M N P U Y R S T W Z SPECIAL_CHARACTERS UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( ) ]
		    
		self.labels5 = ['A O N T D J G Ó I Z S K U B Ą Ć E W Y M Ł H Ś Ń R C P L Ę Ż F Ź UNDO YOUTUBE SAVE SPACJA SPECIAL_CHARACTERS SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( )]

		self.labels6 = [ 'A O U W K J H Ą I Y R C M G Ę Ś E N T P B Ł Ż Ń Z S D L F Ó Ć Ź UNDO YOUTUBE SAVE SPACJA SPECIAL_CHARACTERS SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( )]
		
		self.labels7 = [ 'A O Z W K J Ę Ó I Y R C M G Ą Ś E N T P B F Ż Ń U S D L H Ł Ć Ź UNDO YOUTUBE SAVE SPACJA SPECIAL_CHARACTERS SPEAK EXIT'.split( ), '1 2 3 4 5 6 7 8 9 0 + - * / = % $ & . , ; : " ? ! @ # ( ) [ ] { } < > ~ UNDO YOUTUBE SAVE SPACJA SPEAK EXIT'.split( )]

		self.labels = eval( 'self.labels'+str(self.spellerNumber) )

		self.colouredLabels = [ 'A', 'E', 'I', 'O', 'U', 'Y' ]
		self.colouredLabels2 = [ 'Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż' ]

		if self.con != 0:
			if len( self.labels[ 0 ] ) == 30:
				self.numberOfRows = [ 4, 5 ]
				self.specialButtonsMarker = -3
				self.startIndex = 4
			elif len( self.labels[ 0 ] ) == 39:
				self.numberOfRows = [ 5, 5 ]
				self.specialButtonsMarker = -4
				self.startIndex = 3
			else:
				print 'Blad w definiowaniu tablicy'
				exit( )

			self.numberOfColumns = [ 8, 9 ]

			self.flag = 'row'						
			self.pressFlag = False

			self.rowIteration = 0						
			self.columnIteration = 0							
			self.countRows = 0
			self.countColumns = 0										

			self.maxNumberOfRows = 2
			self.maxNumberOfColumns = 2									

			self.numberOfPresses = 1
			self.subSizerNumber = 0

			if self.control != 'tracker':
				self.mouseCursor = PyMouse( )
				self.mousePosition = self.winWidth - 8 - self.xBorder, self.winHeight - 8 - self.yBorder
				self.mouseCursor.move( *self.mousePosition )			

                        self.replacements = { '-' : ' minus ', 
                                              '+' : ' plus ', 
                                              '*' : ' razy ', 
                                              '/' : ' podzielić na ', 
                                              '=' : ' równa się ', 
                                              '%' : ' procent ', 
                                              '$' : ' dolar', 
                                              '@' : 'małpa', 
                                              '~' : 'tylda', 
                                              '!' : 'wykrzyknik', 
                                              '?' : 'znak zapytania',
                                              '#' : 'kratka', 
                                              '&' : 'handlowe i', 
                                              '(' : 'nawias okrągły otwarcie', 
                                              ')' : 'nawias okrągły zamknięcie', 
                                              '[' : 'nawias kwadratowy otwarcie', 
                                              ']' : 'nawias kwadratowy zamknięcie', 
                                              '{' : 'nawias klamrowy otwarcie', 
                                              '}' : 'nawias klamrowy zamknięcie', 
                                              '<' : 'nawias ostrokątny otwarcie', 
                                              '>' : 'nawias ostrokątny zamknięcie', 
                                              '^' : 'daszek',
                                              ';' : 'średnik', 
                                              ':' : 'dwukropek', 
                                              '\\': 'ukośnik', 
                                              '|' : 'kreska pionowa ', 
                                              '"' : 'cudzysłów', 
                                              '\'': 'apostrof', 
                                              ',' : 'przecinek',
                                              '.' : 'kropka'
                                      }

			mixer.init( )	
			if self.switchSound.lower( ) != 'off' or self.pressSound.lower( ) == 'off':
                                self.switchingSound = mixer.Sound( self.pathToAP + '/sounds/switchSound.ogg' )
                                self.pressingSound = mixer.Sound( self.pathToAP + '/sounds/pressSound.ogg' )
		
				self.phones = glob.glob( self.pathToAP + 'sounds/phone/*' )
				self.phoneLabels = [ item[ item.rfind( '/' )+1 : item.rfind( '.' ) ] for item in self.phones ]
				self.sounds = [ mixer.Sound( self.sound ) for self.sound in self.phones ]
				
				self.rows = glob.glob( self.pathToAP + 'sounds/rows/*' )
				self.rowLabels = [ item[ item.rfind( '/' )+1 : item.rfind( '.' ) ] for item in self.rows ]
				self.rowSounds = [ mixer.Sound( self.sound ) for self.sound in self.rows ]
                                                                
                                self.cofnijSound = mixer.Sound( self.pathToAP + 'sounds/cofnij.ogg' )
                                self.youtubeSound = mixer.Sound( self.pathToAP + 'sounds/youtube.ogg' )
                                self.zapisacSound = mixer.Sound( self.pathToAP + 'sounds/zapisać.ogg' )
                                self.spacjaSound = mixer.Sound( self.pathToAP + 'sounds/spacja.ogg' )
                                self.znakiSound = mixer.Sound( self.pathToAP + 'sounds/znaki specjalne.ogg' )
                                self.czytacSound = mixer.Sound( self.pathToAP + 'sounds/czytać.ogg' )
                                self.wyjscieSound = mixer.Sound( self.pathToAP + 'sounds/wyjście.ogg' )
                                self.usypiamSound = mixer.Sound( self.pathToAP + 'sounds/usypiam.ogg' )

                                self.typewriterKeySound = mixer.Sound( self.pathToAP + 'sounds/typewriter_key.ogg' )
                                self.typewriterForwardSound = mixer.Sound( self.pathToAP + 'sounds/typewriter_forward.ogg' )
                                self.typewriterSpaceSound = mixer.Sound( self.pathToAP + 'sounds/typewriter_space.ogg' )

			self.SetBackgroundColour( 'black' )
		    
	#-------------------------------------------------------------------------
        def initializeBitmaps(self):
            
		if self.specialButtonsMarker == -3:

			labelFiles = [ self.pathToAP + file for file in [ 'icons/speller/special_characters.png', 'icons/speller/undo.png', 'icons/speller/youtube.png', 'icons/speller/save.png', 'icons/speller/speak.png', 'icons/speller/exit.png', ] ]
			labelBitmapIndex = [ self.labels[ 0 ].index( self.labels[ 0 ][ -7 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -6 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -5 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -4 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -2 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -1 ] ) ]
		
		if self.specialButtonsMarker == -4:

			labelFiles = [ self.pathToAP + 'icons/speller/' + item for item in [ 'undo.png', 'youtube.png', 'save.png', 'special_characters.png', 'speak.png', 'exit.png', ] ]
			labelBitmapIndex = [ self.labels[ 0 ].index( self.labels[ 0 ][ -7 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -6 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -5 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -3 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -2 ] ), self.labels[ 0 ].index( self.labels[ 0 ][ -1 ] ) ]

		self.labelBitmaps = { }	    

		for labelFilesIndex, labelIndex in enumerate( labelBitmapIndex ):
			self.labelBitmaps[ self.labels[ 0 ][ labelIndex ] ] = wx.BitmapFromImage( wx.ImageFromStream( open( labelFiles[ labelFilesIndex ], 'rb' )) )      
		labelFiles2 = [ self.pathToAP + 'icons/speller/' + item for item in [ 'special_characters.png', 'undo.png', 'youtube.png', 'save.png', 'speak.png', 'exit.png', ] ]
            
		self.labelBitmaps2 = { }
	    
		labelBitmapIndex2 = [ self.labels[ 1 ].index( self.labels[ 1 ][ -6 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -5 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -4 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -2 ] ), self.labels[ 1 ].index( self.labels[ 1 ][ -1 ] ) ]

		for labelFilesIndex2, labelIndex2 in enumerate( labelBitmapIndex2 ):
			self.labelBitmaps2[ self.labels[ 1 ][ labelIndex2 ] ] = wx.BitmapFromImage( wx.ImageFromStream( open( labelFiles2[ -5: ][ labelFilesIndex2 ], 'rb' )) )

	#-------------------------------------------------------------------------	
	def createGui(self):

		self.thicknessOfExternalBorder = self.xBorder # factor related to the border of the entire board
		self.thicknessOfInternalBorder = self.xBorder # factor related to the border of every button 

		self.textFieldWidth = self.winWidth - 2*self.thicknessOfExternalBorder
		self.textFieldHeight = 0.2 * ( self.winHeight - 20 ) # -20 because of the Unity upper bar

		self.buttonsBoardWidth  = self.winWidth - self.thicknessOfExternalBorder * 2 - self.thicknessOfInternalBorder * ( self.numberOfColumns[ 0 ] - 1 )
		self.buttonsBoardHeight = ( self.winHeight - 20 ) - self.textFieldHeight - self.thicknessOfExternalBorder * 3 - self.thicknessOfInternalBorder * ( self.numberOfRows[ 0 ] - 1 ) # -20 because of the Unity upper bar
		
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		self.textField = wx.TextCtrl( self, style = wx.TE_LEFT, size = (  self.textFieldWidth, self.textFieldHeight ) )
		self.textField.SetFont( wx.Font( self.textFontSize, eval(self.textFont), wx.NORMAL, wx.NORMAL ) )
		self.mainSizer.Add( self.textField, flag = wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border = self.thicknessOfExternalBorder )
		
		self.subSizers = [ ]
		
		subSizer = wx.GridBagSizer( self.xBorder, self.yBorder )

		if self.control != 'tracker':
			event = eval('wx.EVT_LEFT_DOWN')
		else:
			event = eval('wx.EVT_BUTTON')
			
		for index_1, item in enumerate( self.labels[ 0 ][ :-7 ] ):
			b = bt.GenButton( self, -1, item, name = item, size = ( self.buttonsBoardWidth / float( self.numberOfColumns[ 0 ] ), self.buttonsBoardHeight / float( self.numberOfRows[ 0 ] ) ) )
			b.SetFont( wx.Font( self.tableFontSize, eval(self.textFont), wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )

			if item in self.colouredLabels and self.vowelColour != 'False':
				b.SetForegroundColour( self.vowelColour )
			elif item in self.colouredLabels2 and self.polishLettersColour != 'False':
				b.SetForegroundColour( self.polishLettersColour )
			else:
				b.SetForegroundColour( self.textColour )

			b.Bind( event, self.onPress )
			subSizer.Add( b, ( index_1 / self.numberOfColumns[ 0 ], index_1 % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )

		for index_2, item in enumerate( self.labels[ 0 ][ -7 : self.specialButtonsMarker ], start = 1 ):
			b = bt.GenBitmapButton( self, -1, name = item, bitmap = self.labelBitmaps[ item ], size = ( self.buttonsBoardWidth / float( self.numberOfColumns[ 0 ] ), self.buttonsBoardHeight / float( self.numberOfRows[ 0 ] ) ) )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetBezelWidth( 3 )
                        b.Bind( event, self.onPress )
			subSizer.Add( b, ( ( index_1 + index_2 ) / self.numberOfColumns[ 0 ], ( index_1 + index_2 ) % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )

		for item in ( self.labels[ 0 ][ self.specialButtonsMarker ], ):

			if self.specialButtonsMarker == -3:
				b = bt.GenButton( self, -1, item, name = item, size = ( 3 * ( self.buttonsBoardWidth / float( self.numberOfColumns[ 0 ] ) ), self.buttonsBoardHeight / float( self.numberOfRows[ 0 ] ) ) )

			if self.specialButtonsMarker == -4:
				b = bt.GenButton( self, -1, item, name = item, size = ( 2 * ( self.buttonsBoardWidth / float( self.numberOfColumns[ 0 ] ) ), self.buttonsBoardHeight / float( self.numberOfRows[ 0 ] ) ) )
				
			b.SetFont( wx.Font( self.tableFontSize, eval(self.tableFont), wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetForegroundColour( self.textColour )
			b.Bind( event, self.onPress )

			if self.specialButtonsMarker == -3:
				subSizer.Add( b, ( ( index_1 + index_2 ) / self.numberOfColumns[ 0 ], ( index_1 + index_2 + 1 ) % self.numberOfColumns[ 0 ] ), ( 1, 3 ), wx.EXPAND )
			elif self.specialButtonsMarker == -4:
				subSizer.Add( b, ( ( index_1 + index_2 ) / self.numberOfColumns[ 0 ], ( index_1 + index_2 + 1 ) % self.numberOfColumns[ 0 ] ), ( 1, 2 ), wx.EXPAND )

		for index_3, item in enumerate( self.labels[ 0 ][ self.specialButtonsMarker+1: ], start = self.startIndex ):
			b = bt.GenBitmapButton( self, -1, name = item, bitmap = self.labelBitmaps[ item ], size = ( self.buttonsBoardWidth / float( self.numberOfColumns[ 0 ] ), self.buttonsBoardHeight / float( self.numberOfRows[ 0 ] ) ) )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetBezelWidth( 3 )
                        b.Bind( event, self.onPress )
			subSizer.Add( b, ( ( index_1 + index_2 + index_3 ) / self.numberOfColumns[ 0 ], ( index_1 + index_2 + index_3 ) % self.numberOfColumns[ 0 ] ), wx.DefaultSpan, wx.EXPAND )

		self.subSizers.append( subSizer )		    
		self.mainSizer.Add( self.subSizers[ 0 ], proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border = self.yBorder)
		self.SetSizer( self.mainSizer )
		self.Center( )
		
		subSizer2 = wx.GridBagSizer( self.xBorder, self.yBorder )

		self.buttonsBoardWidth2  = self.winWidth - self.thicknessOfExternalBorder * 2 - self.thicknessOfInternalBorder * ( self.numberOfColumns[ 1 ] - 1 )
		self.buttonsBoardHeight2 = ( self.winHeight - 20 ) - self.textFieldHeight - self.thicknessOfExternalBorder * 3 - self.thicknessOfInternalBorder * ( self.numberOfRows[ 1 ] - 1 ) # -20 because of the Unity upper bar

		for index_1, item in enumerate( self.labels[ 1 ][ :-6 ] ):
			b = bt.GenButton( self, -1, item, name = item, size = ( self.buttonsBoardWidth2 / float( self.numberOfColumns[ 1 ] ), self.buttonsBoardHeight2 / float( self.numberOfRows[ 1 ] ) ) )
			b.SetFont( wx.Font( self.tableFontSize, eval(self.tableFont), wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetForegroundColour( self.textColour )
			b.Bind( event, self.onPress )
			subSizer2.Add( b, ( index_1 / self.numberOfColumns[ 1 ], index_1 % self.numberOfColumns[ 1 ] ), wx.DefaultSpan, wx.EXPAND )

		for index_2, item in enumerate( self.labels[ 1 ][ -6 : -3 ], start = 1 ):
			b = bt.GenBitmapButton( self, -1, name = item, bitmap = self.labelBitmaps2[ item ], size = ( self.buttonsBoardWidth2 / float( self.numberOfColumns[ 1 ] ), self.buttonsBoardHeight2 / float( self.numberOfRows[ 1 ] ) ) )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetBezelWidth( 3 )
                        b.Bind( event, self.onPress )
			subSizer2.Add( b, ( ( index_1 + index_2 ) / self.numberOfColumns[ 1 ], ( index_1 + index_2 ) % self.numberOfColumns[ 1 ] ), wx.DefaultSpan, wx.EXPAND )

		for item in ( self.labels[ 1 ][ -3 ], ):
			b = bt.GenButton( self, -1, item, name = item, size = ( 3 * (self.buttonsBoardWidth2 / float( self.numberOfColumns[ 1 ] )), self.buttonsBoardHeight2 / float( self.numberOfRows[ 1 ] ) ) )
			b.SetFont( wx.Font( self.tableFontSize, eval(self.tableFont), wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,  False ) )
			b.SetBezelWidth( 3 )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetForegroundColour( self.textColour )
			b.Bind( event, self.onPress )
			subSizer2.Add( b, ( ( index_1 + index_2 ) / self.numberOfColumns[ 1 ], ( index_1 + index_2 + 1 ) % self.numberOfColumns[ 1 ] ), ( 1, 4 ), wx.EXPAND )

		for index_3, item in enumerate( self.labels[ 1 ][ -2: ], start = 5 ):
			b = bt.GenBitmapButton( self, -1, name = item, bitmap = self.labelBitmaps2[ item ], size = ( self.buttonsBoardWidth / float( self.numberOfColumns[ 1 ] ), self.buttonsBoardHeight / float( self.numberOfRows[ 1 ] ) ) )
			b.SetBackgroundColour( self.backgroundColour )
			b.SetBezelWidth( 3 )
                        b.Bind( event, self.onPress )
			subSizer2.Add( b, ( ( index_1 + index_2 + index_3 ) / self.numberOfColumns[ 1 ], ( index_1 + index_2 + index_3 ) % self.numberOfColumns[ 1 ] ), wx.DefaultSpan, wx.EXPAND )

		self.subSizers.append( subSizer2 )		   
		self.mainSizer.Add( self.subSizers[ 1 ], proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border = self.yBorder )

		if self.subSizerNumber == 0:
			self.mainSizer.Show( item = self.subSizers[ 1 ], show = False, recursive = True )
		else:
			self.mainSizer.Show( item = self.subSizers[ 0 ], show = False, recursive = True )

		self.SetSizer( self.mainSizer )
		self.Center( )

	#-------------------------------------------------------------------------
	def initializeTimer(self):
		self.stoper = wx.Timer( self )
		self.Bind( wx.EVT_TIMER, self.timerUpdate, self.stoper )

		if self.control != 'tracker':
			self.stoper.Start( self.timeGap )
	
	#-------------------------------------------------------------------------
	def getLabels(self):
		return self.labels

	#-------------------------------------------------------------------------
	def createBindings(self):
		self.Bind( wx.EVT_CLOSE, self.OnCloseWindow )
	
	#-------------------------------------------------------------------------
	def OnCloseWindow(self, event):

		if self.control != 'tracker':
			if True in [ 'debian' in item for item in os.uname( ) ]: #POSITION OF THE DIALOG WINDOW DEPENDS ON WINDOWS MANAGER NOT ON DESKTOP ENVIROMENT. THERE IS NO REASONABLE WAY TO CHECK IN PYTHON WHICH WINDOWS MANAGER IS CURRENTLY RUNNING, BESIDE IT IS POSSIBLE TO FEW WINDOWS MANAGER RUNNING AT THE SAME TIME. I DON'T SEE SOLUTION OF THIS ISSUE, EXCEPT OF CREATING OWN SIGNAL (AVR MICROCONTROLLERS).
				if os.environ.get('KDE_FULL_SESSION'):
					self.mousePosition = self.winWidth/1.7, self.winHeight/1.7
				# elif ___: #for gnome-debian
				# 	self.mousePosition = self.winWidth/6.5, self.winHeight/6.
				else:
					self.mousePosition = self.winWidth/1.8, self.winHeight/1.7
			else:
				self.mousePosition = self.winWidth/1.9, self.winHeight/1.68
			
		self.mouseCursor.move( *self.mousePosition )
			
		dial = wx.MessageDialog(self, 'Czy napewno chcesz wyjść z programu?', 'Wyjście',
					wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION | wx.STAY_ON_TOP)
            
		ret = dial.ShowModal()
		
		if ret == wx.ID_YES:
			try:
				if "smplayer" in [psutil.Process(i).name() for i in psutil.pids( )]:
					os.system( 'smplayer -send-action quit' )
			except TypeError:
				if "smplayer" in [psutil.Process(i).name for i in psutil.pids( )]:
					os.system( 'smplayer -send-action quit' )

			if __name__ == '__main__':
				self.Destroy()
			else:
				self.parent.Destroy( )
				self.Destroy( )
		else:
			event.Veto()

			if self.control != 'tracker':
				self.mousePosition = self.winWidth - 8 - self.yBorder, self.winHeight - 8 - self.xBorder
				self.mouseCursor.move( *self.mousePosition )	

	#-------------------------------------------------------------------------
	def onExit(self):
		if __name__ == '__main__':
			self.stoper.Stop( )
			self.Destroy( )
		else:
			if self.con != 0:
				self.stoper.Stop( )

				if self.parent:
					self.parent.Show( True )

					if self.control != 'tracker':
						self.parent.stoper.Start( self.parent.timeGap )

			self.MakeModal( False )
			self.Destroy( )
		
	#-------------------------------------------------------------------------
	def onPress(self, event):
		
		if self.pressSound.lower( ) != 'off':
			self.pressingSound.play( )

		if self.control == 'tracker':
			if self.pressFlag == False:
				self.button = event.GetEventObject()
				self.button.SetBackgroundColour( self.selectionColour )
				self.pressFlag = True
				self.label = event.GetEventObject().GetName().encode( 'utf-8' )			
				self.stoper.Start( 0.15 * self.timeGap )

				if self.label == 'SPECIAL_CHARACTERS':								
                                        if self.pressSound.lower() == 'voice':
                                                self.znakiSound.play()

					self.subSizerNumber = 1

					self.mainSizer.Show( item = self.subSizers[ 1 ], show = True, recursive = True )
					self.mainSizer.Show( item = self.subSizers[ 0 ], show = False, recursive = True )					
					self.SetSizer( self.mainSizer )

					self.Layout( )

				elif self.label == 'UNDO':
                                        if self.pressSound.lower() == 'voice':
                                                self.cofnijSound.play()

					self.typewriterForwardSound.play( )
					self.textField.Remove( self.textField.GetLastPosition( ) - 1, self.textField.GetLastPosition( ) )

				elif self.label == 'YOUTUBE':								
                                        if self.pressSound.lower() == 'voice':
                                                self.youtubeSound.play()
					text = self.textField.GetValue().encode('utf-8')
                                        os.system('minitube %s &' %text)

					self.stoper.Stop()
					self.Hide()
					self.menu = minitubePilot.pilot( self, id =1 )
					
					self.menu.Show()

				elif self.label == 'SAVE':
                                        if self.pressSound.lower() == 'voice':
                                                self.zapisacSound.play()

					text = str( self.textField.GetValue( ) )

					if text == '':
						pass
					else:
						f = open( 'myTextFile.txt', 'w' )
						f.write( self.textField.GetValue( ) )
						f.close( )

				elif self.label == 'SPACJA':
                                        if self.pressSound.lower() == 'voice':
                                                self.spacjaSound.play()

					self.typewriterSpaceSound.play( )
					self.textField.AppendText( ' ' )

				elif self.label == 'SPEAK':
                                        if self.pressSound.lower() == 'voice':
                                                self.czytacSound.play()

					text = str( self.textField.GetValue( ) )

					if text == '' or text.isspace( ):
						pass

					else:
						textToSpeech = reduce( lambda text, replacer: text.replace( *replacer ), self.replacements.iteritems( ), text )
						time.sleep( 1 )
						os.system( 'milena_say %s' %textToSpeech )
					# try:
					# 	textToLoad = open( 'myTextFile.txt' ).read( )
					# 	self.textField.Clear( )
					# 	self.textField.AppendText( textToLoad )

					# except IOError:
					# 	pass

				elif self.label == 'EXIT':
                                        if self.pressSound.lower() == 'voice':
                                                self.wyjscieSound.play()

					if self.subSizerNumber == 0:
						self.onExit( )

					else:	
					    self.mainSizer.Show( item = self.subSizers[ self.subSizerNumber ], show = False, recursive = True )

					    self.subSizerNumber = 0
					    self.mainSizer.Show( item = self.subSizers[ self.subSizerNumber ], show = True, recursive = True )

					    self.SetSizer( self.mainSizer )
					    self.Layout( )

				else:
                                        textToSpeech = reduce( lambda text, replacer: text.replace( *replacer ), self.replacements.iteritems( ), self.label )
                                        time.sleep( 1 )
                                        self.typewriterKeySound.play( )
                                        os.system( 'milena_say %s' %textToSpeech )
                                        
                                        
                                        self.textField.AppendText( self.label )
			else:
				pass
		else:
			
                        self.numberOfPresses += 1

			if self.numberOfPresses == 1:

				if self.flag == 'rest':
					self.flag = 'row'
					self.rowIteration = 0

				elif self.flag == 'row':

					if self.switchSound.lower() == 'voice':
						for idx, item in enumerate( self.rowLabels ):
							if int(item) == self.rowIteration:
								self.rowSounds[ idx ].play( )
								break

					if self.rowIteration != self.numberOfRows[ self.subSizerNumber ]:

						buttonsToHighlight = range( ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ], ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ] + self.numberOfColumns[ self.subSizerNumber ] )
					else:
						if self.specialButtonsMarker == -3 or self.subSizerNumber == 1:
							buttonsToHighlight = range( ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ], ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ] + 6 )

						elif self.specialButtonsMarker == -4:
							buttonsToHighlight = range( ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ], ( self.rowIteration - 1 ) * self.numberOfColumns[ self.subSizerNumber ] + 7 )

						# elif self.subSizerNumber == 1:
						# 	buttonsToHighlight = range( ( self.rowIteration ) * self.numberOfColumns[ self.subSizerNumber ], ( self.rowIteration ) * self.numberOfColumns[ self.subSizerNumber ] + 6 )

					for button in buttonsToHighlight:
						item = self.subSizers[ self.subSizerNumber ].GetItem( button )
						b = item.GetWindow( )
						b.SetBackgroundColour( self.selectionColour )
						b.SetFocus( )

					self.flag = 'columns' 
					self.rowIteration -= 1
					self.columnIteration = 0

				elif self.flag == 'columns' and self.rowIteration != self.numberOfRows[ self.subSizerNumber ] - 1:

					item = self.subSizers[ self.subSizerNumber ].GetItem( ( self.rowIteration ) * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration - 1 )
					b = item.GetWindow( )
					b.SetBackgroundColour( self.selectionColour )
					b.SetFocus( )

					label = self.labels[ self.subSizerNumber ][ self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration - 1 ]
					
					if self.specialButtonsMarker == -3:
						if label == 'SPECIAL_CHARACTERS':								

							self.subSizerNumber = 1

							self.mainSizer.Show( item = self.subSizers[ 1 ], show = True, recursive = True )
							self.mainSizer.Show( item = self.subSizers[ 0 ], show = False, recursive = True )					
							self.SetSizer( self.mainSizer )

							self.Layout( )

						else:
                                                        textToSpeech = reduce( lambda text, replacer: text.replace( *replacer ), self.replacements.iteritems( ), label )
                                                        time.sleep( 1 )
							self.typewriterKeySound.play( )
                                                        os.system( 'milena_say %s' %textToSpeech )

							self.textField.AppendText( label )

					else:
                                                textToSpeech = reduce( lambda text, replacer: text.replace( *replacer ), self.replacements.iteritems( ), label )
                                                time.sleep( 1 )
						self.typewriterKeySound.play( )
                                                os.system( 'milena_say %s' %textToSpeech )

						self.textField.AppendText( label )

					self.flag = 'row'
					self.rowIteration = 0
					self.columnIteration = 0
					self.countColumns = 0

				elif self.flag == 'columns' and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1:

					item = self.subSizers[ self.subSizerNumber ].GetItem( ( self.rowIteration ) * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration-1 )
					b = item.GetWindow( )
					b.SetBackgroundColour( self.selectionColour )
					b.SetFocus( )

					label = self.labels[ self.subSizerNumber ][ self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration-1 ]

					if label == 'UNDO':
                                                if self.pressSound.lower() == 'voice':
                                                        self.cofnijSound.play()
						self.typewriterForwardSound.play( )
						self.textField.Remove( self.textField.GetLastPosition( ) - 1, self.textField.GetLastPosition( ) )

					elif label == 'YOUTUBE':
                                                if self.pressSound.lower() == 'voice':
                                                        self.youtubeSound.play()
                                                text = self.textField.GetValue().encode('utf-8')

                                                os.system('minitube %s &' %text)
                                                time.sleep(0.5)
                                                os.system("sleep 1")

                                                self.stoper.Stop()
                                                self.Hide()
                                                
                                                self.menu = minitubePilot.pilot( self, id =1 )
                                                
                                                self.menu.Show()

					elif label == 'SAVE':
                                                if self.pressSound.lower() == 'voice':
                                                        self.zapisacSound.play()

						text = str( self.textField.GetValue( ) )
						if text == '':
							pass
						else:
							f = open( 'myTextFile.txt', 'w' )
							f.write( self.textField.GetValue( ) )
							f.close( )

					elif label == 'SPACJA':
                                                if self.pressSound.lower() == 'voice':
                                                        self.spacjaSound.play()

						self.typewriterSpaceSound.play( )
						self.textField.AppendText( ' ' )

					elif label == 'SPEAK':
                                                if self.pressSound.lower() == 'voice':
                                                        self.czytacSound.play()
                                                text = str( self.textField.GetValue( ) )

                                                if text == '' or text.isspace( ):
                                                        pass

                                                else:
                                                        textToSpeech = reduce( lambda text, replacer: text.replace( *replacer ), replacements.iteritems( ), text )
                                                        
                                                        time.sleep( 1 )
                                                        os.system( 'milena_say %s' %textToSpeech )
                                                        # try:
                                                        # 	textToLoad = open( 'myTextFile.txt' ).read( )
                                                        # 	self.textField.Clear( )
                                                        # 	self.textField.AppendText( textToLoad )

                                                        # except IOError:
                                                        # 	print "Can't find the file"
                                                        # 	pass

					elif label == 'EXIT':
                                                if self.pressSound.lower() == 'voice':
                                                        self.wyjscieSound.play()
						if self.subSizerNumber == 0:
							self.onExit( )

						else:	
						    self.mainSizer.Show( item = self.subSizers[ self.subSizerNumber ], show = False, recursive = True )

						    self.subSizerNumber = 0
						    self.mainSizer.Show( item = self.subSizers[ self.subSizerNumber ], show = True, recursive = True )

						    self.SetSizer( self.mainSizer )
						    self.Layout( )

					elif self.specialButtonsMarker == -4:
						if label == 'SPECIAL_CHARACTERS':								
                                                        if self.pressSound.lower() == 'voice':
                                                                self.znakiSound.play()

							self.subSizerNumber = 1

							self.mainSizer.Show( item = self.subSizers[ 1 ], show = True, recursive = True )
							self.mainSizer.Show( item = self.subSizers[ 0 ], show = False, recursive = True )					
							self.SetSizer( self.mainSizer )

							self.Layout( )

					self.flag = 'row'
					self.rowIteration = 0
					self.columnIteration = 0
					self.countRows = 0
					self.countColumns = 0

			else:
				event.Skip( ) #Event skip use in else statement here!			

	#-------------------------------------------------------------------------
	def timerUpdate(self, event):

		if self.control == 'tracker':

			if self.button.GetBackgroundColour( ) == self.backgroundColour:
				self.button.SetBackgroundColour( self.selectionColour )
				
			else:
				self.button.SetBackgroundColour( self.backgroundColour )	

			self.stoper.Stop( )
			self.pressFlag = False

		else:
			if self.control != 'tracker':
				self.mouseCursor.move( *self.mousePosition )

			self.numberOfPresses = 0		

			if self.flag == 'row':

				if self.countRows == self.maxNumberOfRows:
                                        if self.switchSound.lower() == 'voice':
                                                self.usypiamSound.play()

					self.flag = 'rest'
					self.countRows = 0

					items = self.subSizers[ self.subSizerNumber ].GetChildren( )
					for item in items:
						b = item.GetWindow( )
						b.SetBackgroundColour( self.backgroundColour )
						b.SetFocus( )

				else:
					self.rowIteration = self.rowIteration % self.numberOfRows[ self.subSizerNumber ]

					items = self.subSizers[ self.subSizerNumber ].GetChildren( )
					for item in items:
						b = item.GetWindow( )
						b.SetBackgroundColour( self.backgroundColour )
						b.SetFocus( )

					if self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1:
						self.countRows += 1

						if self.specialButtonsMarker == -3 or self.subSizerNumber == 1:
							buttonsToHighlight = range( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ], self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + 6 )
						elif self.specialButtonsMarker == -4:
							buttonsToHighlight = range( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ], self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + 7 )

					else:
						buttonsToHighlight = range( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ], self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.numberOfColumns[ self.subSizerNumber ] )

					for button in buttonsToHighlight:
						item = self.subSizers[ self.subSizerNumber ].GetItem( button )
						b = item.GetWindow( )
						b.SetBackgroundColour( self.scanningColour )
						b.SetFocus( )

					self.rowIteration += 1

					if self.switchSound.lower( ) == 'on':
						self.switchingSound.play( )

					elif self.switchSound.lower() == 'voice':
						for idx, item in enumerate( self.rowLabels ):
							if int(item) == self.rowIteration:
								self.rowSounds[ idx ].play( )
								break

			elif self.flag == 'columns':
				
				if self.countColumns == self.maxNumberOfColumns:
					self.flag = 'row'

					item = self.subSizers[ self.subSizerNumber ].GetItem( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration - 1 )
					b = item.GetWindow( )
					b.SetBackgroundColour( self.backgroundColour )

					self.rowIteration = 0
					self.countRows =0 
					self.columnIteration = 0
					self.countColumns = 0

				else:
					if (self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 1 and self.rowIteration != self.numberOfRows[ self.subSizerNumber] - 1) or (self.subSizerNumber == 0 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 3 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 and self.specialButtonsMarker == -3) or ( self.subSizerNumber == 1 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 4 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 ) or (self.subSizerNumber == 0 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 2 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 and self.specialButtonsMarker == -4):
						self.countColumns += 1
						
					if self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] or ( self.subSizerNumber == 0 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 2 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 and self.specialButtonsMarker == -3) or ( self.subSizerNumber == 1 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 3 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 ) or ( self.subSizerNumber == 0 and self.columnIteration == self.numberOfColumns[ self.subSizerNumber ] - 1 and self.rowIteration == self.numberOfRows[ self.subSizerNumber ] - 1 and self.specialButtonsMarker == -4):
						self.columnIteration = 0

					items = self.subSizers[ self.subSizerNumber ].GetChildren( )
					for item in items:
						b = item.GetWindow( )
						b.SetBackgroundColour( self.backgroundColour )
						b.SetFocus( )

					item = self.subSizers[ self.subSizerNumber ].GetItem( self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration )
					b = item.GetWindow( )
					b.SetBackgroundColour( self.scanningColour )
					b.SetFocus( )
                                        label = b.Name
                                        
					if self.switchSound.lower( ) == 'on':
						self.switchingSound.play( )

					elif self.switchSound.lower( ) == 'voice':
                                                if label == 'UNDO':
                                                        self.cofnijSound.play()
                                                        
                                                elif label == 'YOUTUBE':
                                                        self.youtubeSound.play()

                                                elif label == 'SAVE':
                                                        self.zapisacSound.play()

                                                elif label == 'SPACJA':
                                                        self.spacjaSound.play()

                                                elif label == 'SPEAK':
                                                        self.czytacSound.play()

                                                elif label == 'EXIT':
                                                        self.wyjscieSound.play()
                                        
                                                elif label == 'SPECIAL_CHARACTERS':								
                                                        self.znakiSound.play()

                                                else:
                                                        
                                                        label = self.labels[ self.subSizerNumber ][ self.rowIteration * self.numberOfColumns[ self.subSizerNumber ] + self.columnIteration ]

                                                        try:
                                                                soundIndex = self.phoneLabels.index( [ item for item in self.phoneLabels if item == label ][ 0 ] )
                                                                sound = self.sounds[ soundIndex ]
                                                                sound.play( )

                                                        except IndexError:
                                                                text = label
                                                                textToSpeech = reduce( lambda text, replacer: text.replace( *replacer ), self.replacements.iteritems( ), text )
                                                                os.system('milena_say %s' %textToSpeech)

					self.columnIteration += 1
					
			else:
				pass

# #=============================================================================

# #==========================================================================================================================================================
# #			
# #			This class was created because of the strange behaviour of SetTransparent method on Ubuntu 11.04 and up 
# #
# #==========================================================================================================================================================

# class suspend(wx.Frame):
# 	def __init__(self, parent, id):

# 	    self.dw, self.dh = wx.DisplaySize()
	    	    
#             wx.Frame.__init__(self , parent , id, 'Pilot', size = (210, 280), pos = (self.dw - 230, self.dh - 325) )
	    
#             style = self.GetWindowStyle()
#             self.SetWindowStyle( style | wx.STAY_ON_TOP )

# 	    #Publisher().subscribe( self.setP, ( 'radioID' ) ) #connect to a signal called 'playButtonPosition'
	    
#             self.parent = parent
#             self.MakeModal( True )		
		
#             self.initializeParameters()				
            
#             self.createGui()								
#             self.initializeTimer()					

# 	    self.Show(True)
# 	    self.SetTransparent( 0 )

# 	#-------------------------------------------------------------------------
# 	def initializeParameters(self):

#             self.timeGap = 2000
            
#             self.mouseCursor = PyMouse()
#             self.mouseCursor.move( self.dw - 225, self.dh - 265 )	

# 	#-------------------------------------------------------------------------
# 	def createGui(self):

# 		self.mainSizer = wx.BoxSizer( wx.VERTICAL )

# 		self.subSizer = wx.GridBagSizer( 4, 4 )
		
#                 b = bt.GenButton( self, -1, '', name='' )
#                 b.Bind( wx.EVT_LEFT_DOWN, self.onPress )
				    
#                 self.subSizer.Add(b, ( 0, 0 ), wx.DefaultSpan, wx.EXPAND)
			
#                 self.subSizer.AddGrowableRow( 0 )
#                 self.subSizer.AddGrowableCol( 0 )
		
# 		self. mainSizer.Add( self.subSizer, proportion=1, flag=wx.EXPAND )
# 		self.SetSizer( self. mainSizer )
                    
# 	#-------------------------------------------------------------------------
# 	def initializeTimer(self):
# 		self.stoper = wx.Timer(self)
# 		self.Bind( wx.EVT_TIMER , self.timerUpdate , self.stoper )
# 		self.stoper.Start( self.timeGap )
	
# 	#-------------------------------------------------------------------------
# 	def onExit(self):
# 		self.stoper.Stop()
# 		self.MakeModal( False )
# 		self.parent.Show()
# 		self.parent.stoper.Start( self.parent.timeGap )
# 		self.Destroy()

#         #-------------------------------------------------------------------------
# 	def setP(self, message):
# 		self.radioID = message.data
	
# 	#-------------------------------------------------------------------------
#         def onPress(self, event):
#             self.stoper.Stop()
#             self.menu = pilot(self, id=2)
	    
# 	    #self.message = self.radioID
# 	    #Publisher().sendMessage( ( 'radioID' ), self.message ) #call the Publisher object’s sendMessage method and pass it the topic string and the message in order to send the message
            
#             self.Hide()
#             self.menu.Show()	

# 	#-------------------------------------------------------------------------
# 	def timerUpdate(self , event):
            
#                	self.mouseCursor.move( self.dw - 225, self.dh - 265 )	

#=============================================================================
if __name__ == '__main__':

	app = wx.App(False)
	frame = youtube2( parent = None, id = -1 )
	frame.Show( True )
	app.MainLoop( )
