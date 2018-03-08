package com.ifroglab.lora;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.TextEvent;
import java.awt.event.TextListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;

import javax.swing.JFileChooser;


public class preference extends Frame
{
	// UI
	private TextField TextFieldUrl;
	private Checkbox  checkBoxSaveLog;
	private Checkbox  checkBoxUpload;
	private Checkbox  checkBoxDashboard;
	private Checkbox  checkBoxMQTT;
	private Button    ButtonLogFileName;  
	private Choice    mChoicePower;
	
	// "final" variables are constants
	static final int H_SIZE = 500;
	static final int V_SIZE = 490;
	private Frame mainFrame;
	private ifroglablora mLo;
	private TextField TextFieldmHz;
			
	
	public preference(ifroglablora iifroglablora)
	{
		   mLo=iifroglablora;
	       // Begin 01, 設定主畫面UI
		   mainFrame= new Frame();  
		   mainFrame = new Frame(mLo.mStr[14][mLo.lan]);
		   mainFrame.addWindowListener(new WindowAdapter() {         // 關閉按鈕
		       public void windowClosing(WindowEvent windowEvent){
		    	   		mainFrame.dispose();
		    	   // System.exit(0);
		    	   //    dispose();
		       }
		   });
		   mainFrame.setSize(H_SIZE,V_SIZE);  
		   mainFrame.setMinimumSize(new Dimension(H_SIZE,V_SIZE));
		   mainFrame.setMaximumSize(new Dimension(H_SIZE,V_SIZE));
		   mainFrame.setResizable(false);
		   
		   mainFrame.setLayout(null);  
		   ui_Step1(mainFrame);
		   ui_Step2(mainFrame);
		   ui_Step3(mainFrame);
		   mainFrame.setVisible(true);  
		   mainFrame.addComponentListener(new ComponentListener() {
			    public void componentResized(ComponentEvent e) {  }
				@Override
				public void componentMoved(ComponentEvent e) {}
				@Override
				public void componentShown(ComponentEvent e) {}
				@Override
				public void componentHidden(ComponentEvent e) {}
			});
		   // END 01
	}
	
	public void ui_Step1(Frame mainFrame) {

		 int tUITop=0;
		 int y=0;
		 // Begin 01,              添加文字 "Step3"
	     Label l1 = new Label();
	     l1.setAlignment(Label.LEFT);
	     l1.setText(mLo.mStr[56][mLo.lan]);    //"Step3"
	     l1.setSize(140,25);
	     mainFrame.add(l1);  
	     l1.setLocation(10, y+50+tUITop);
	     // end 01                添加Step 3 的文字 "Step3"
		 // Begin 02,              添加文字 "Step3"
	     Label l2 = new Label();
	     l2.setAlignment(Label.LEFT);
	     l2.setText(mLo.mStr[57][mLo.lan]);    //"Step3"
	     l2.setSize(140,25);
	     mainFrame.add(l2);  
	     l2.setLocation(10, y+75+tUITop);
	     // end 01                添加Step 3 的文字 "Step3"
	     
	     
	      // Begin 03,               添加Step 2  改變語言
	      final Choice ChoiceLanguage=new Choice();  
	      ChoiceLanguage.setBounds(100,100,100,30);  
	      ChoiceLanguage.add("English");             
	      ChoiceLanguage.add("Chinese");       
	      mainFrame.add(ChoiceLanguage);  
	      ChoiceLanguage.setLocation(150,y+55+tUITop+(ChoiceLanguage.size().height/2));
	      ChoiceLanguage.select(mLo.lan);
	      ChoiceLanguage.addItemListener(new ItemListener(){
			@Override
			public void itemStateChanged(ItemEvent e) {
				String t1= Integer.toString(ChoiceLanguage.getSelectedIndex() );   // ChoiceLanguage.getSelectedIndex()   //ChoiceLanguage.getItem(ChoiceLanguage.getSelectedIndex());	
				mLo.FunPreferencesSave("Language",t1 );

                MsgDialog aboutDialog = new MsgDialog(mainFrame,mLo.mStr[58][mLo.lan],500,100 );
                aboutDialog.setVisible(true);
				// System.exit(0);
			}
	      });
	      // END 03
	      // Begin 4,                 添加Step 1 一條區分線
		   Label lineLabel = new Label();
		   lineLabel.setAlignment(Label.LEFT);
		   lineLabel.setText("");     // "Select LoRa device"
		   lineLabel.setSize(H_SIZE,1);
		   lineLabel.setBackground(Color.lightGray );
		   mainFrame.add(lineLabel);  
		   lineLabel.setLocation(0, y+100+tUITop);
		   // END 4
	}

	public void ui_Step2(Frame mainFrame) {
		 int tUITop=30+90;
		 int y=0;

	     // Begin 01,                添加文字 "LoRa 設定"
	     Label l1 = new Label();
	     l1.setAlignment(Label.LEFT);
	     l1.setText(mLo.mStr[49][mLo.lan]);    //"Step3"
	     l1.setSize(100,25);
	     mainFrame.add(l1);  
	     l1.setLocation(10, y+0+tUITop);
	      // END 01
	     
	     // Begin 01,                添加文字 "頻率"
	     Label l2 = new Label();
	     l2.setAlignment(Label.LEFT);
	     l2.setText(mLo.mStr[50][mLo.lan]);    //"Step3"
	     l2.setSize(300,25);
	     mainFrame.add(l2);  
	     l2.setLocation(10, y+30+tUITop);
	      // END 01    
	     
	     // Begin 08, 網址 
	     TextFieldmHz=new TextField(mLo.mStr[48][mLo.lan]);  
	     TextFieldmHz.setBounds(80,150, 80,30);  
	     mainFrame.add(TextFieldmHz);
	     TextFieldmHz.setText(mLo.Frequency);
	     TextFieldmHz.setLocation(320, y+30+tUITop);
	     TextFieldmHz.addTextListener(
	    		 new TextListener() {
				@Override
				public void textValueChanged(TextEvent e) { 
					String tFrequency=TextFieldmHz.getText();
					if(tFrequency.length()>0) {
						float tfloatFrequency = Float.parseFloat(tFrequency);
						if(tfloatFrequency>=137.00f && tfloatFrequency<=1020.00f) {
							mLo.Frequency=tFrequency;
							mLo.FunPreferencesSave("Frequency",tFrequency);
							System.out.println("Entered text: " + tFrequency);
						}
					}
				}
	    		 }
	      );
	     // END 08
	     
	     
	     // Begin 01,                添加文字 "頻率"
	     Label l3 = new Label();
	     l3.setAlignment(Label.LEFT);
	     l3.setText(mLo.mStr[51][mLo.lan]);    //"Step3"
	     l3.setSize(150,25);
	     mainFrame.add(l3);  
	     l3.setLocation(10, y+60+tUITop);
	      // END 01   
	     
	     
	     // Begin 09,               選取 "頻率"
		   mChoicePower=new Choice();  
		   mChoicePower.setBounds(100,100, 120,30);
		   for(int i=0;i<=15;i++) {
			   mChoicePower.add( Integer.toString(i+2)+" dBm");
		   }
		   mChoicePower.select(mLo.Power);
		   mainFrame.add(mChoicePower);  
		   mChoicePower.setLocation(270, 60+tUITop); //+(mChoicePower.size().height/2));
		   mChoicePower.addItemListener(new ItemListener(){
				@Override
				public void itemStateChanged(ItemEvent e) {
					System.out.println(mChoicePower.getItem(mChoicePower.getSelectedIndex()));
					int t1=mChoicePower.getSelectedIndex();
					mLo.FunPreferencesSave("Power",Integer.toString(t1));
				}
		   });
		
		   // END 09
 		 // Begin 5,                 添加Step 1 一條區分線
 		   Label lineLabel = new Label();
 		   lineLabel.setAlignment(Label.LEFT);
 		   lineLabel.setText("");     // "Select LoRa device"
 		   lineLabel.setSize(H_SIZE,1);
 		   lineLabel.setBackground(Color.lightGray );
 		   mainFrame.add(lineLabel);  
 		   lineLabel.setLocation(0, 90+tUITop);
 		   // END 5
	}
	public void ui_Step3(Frame mainFrame) {
		 int tUITop=70;
		 int y=150;

	     // Begin 01,              添加文字 "Step3"
	     Label l1 = new Label();
	     l1.setAlignment(Label.LEFT);
	     l1.setText(mLo.mStr[52][mLo.lan]);    //"Step3"
	     l1.setSize(150,25);
	     mainFrame.add(l1);  
	     l1.setLocation(10, y+0+tUITop);
	     // end 01                添加Step 3 的文字 "Step3"
	     
	    
		 // Begin 06, 上傳到網路的選項 
         checkBoxDashboard = new Checkbox();
         checkBoxDashboard.setLabel(mLo.mStr[45][mLo.lan]);
         checkBoxDashboard.setSize(170,30);
		 mainFrame.add(checkBoxDashboard);
		 checkBoxDashboard.setState(Boolean.parseBoolean(mLo.FunPreferencesLoad("checkBoxDashboard","true")));
		 checkBoxDashboard.setLocation(10, y+30+tUITop);
		 checkBoxDashboard.addItemListener(new ItemListener() {
	         public void itemStateChanged(ItemEvent e) {             
	        	 	System.out.println(" Checkbox: " + (e.getStateChange()==1?"checked":"unchecked"));
	        	 	String tcheck="false";
	         	if (e.getStateChange()==1) { 		tcheck="true";   	 	}
	         	mLo.FunPreferencesSave("checkBoxDashboard",tcheck);
	         }
	      });
		 
		 
		 

		 
			 
		 // END 06	
		 // Begin 07, 打開儀表版的按鈕 
	     Button ButtonIoT = new Button(mLo.mStr[46][mLo.lan]);    //"reflash"
	     ButtonIoT.setBounds(100,100, 140,30); 
	     ButtonIoT.setLocation(280, y+30+tUITop);
	     mainFrame.add(ButtonIoT);
	     //mUIComPortName.setBounds(100,100, 150,75); 
	     //ButtonIoT.setLocation(300,y+190+tUITop);
	     ButtonIoT.addActionListener(new ActionListener() {
	        public void actionPerformed(ActionEvent e) {
	        	 if (Desktop.isDesktopSupported()) {     // 打开Dashboard
		    		    try {
							Desktop.getDesktop().browse(new URI(mLo.mURL[7]+mLo.ProjectId));
						} catch (IOException e1) {e1.printStackTrace();
						} catch (URISyntaxException e1) {	e1.printStackTrace();}
		    	  }
	        	 
	        }
	     });
	     // END 07
	         
		 // Begin 06, 上傳到網路的選項 
         checkBoxUpload = new Checkbox();
         checkBoxUpload.setLabel(mLo.mStr[53][mLo.lan]);
         checkBoxUpload.setSize(250,30);
		 mainFrame.add(checkBoxUpload);
		 checkBoxUpload.setState(Boolean.parseBoolean(mLo.FunPreferencesLoad("checkBoxUpload","false")));
		 checkBoxUpload.setLocation(10, y+60+tUITop);
		 checkBoxUpload.addItemListener(new ItemListener() {
	         public void itemStateChanged(ItemEvent e) {             
	        	 	System.out.println(" Checkbox: " + (e.getStateChange()==1?"checked":"unchecked"));
	        	 	String tcheck="false";
	         	if (e.getStateChange()==1) { 		tcheck="true";   	 	}
	         	mLo.FunPreferencesSave("checkBoxUpload",tcheck);
	         }
	      });
		 // END 06	
         // Begin 08, 網址 
	     TextFieldUrl=new TextField(mLo.mStr[48][mLo.lan]);  
	     TextFieldUrl.setBounds(280,150, 440,30);  
	     mainFrame.add(TextFieldUrl);
	     TextFieldUrl.setLocation(50, y+90+tUITop);
	     // END 08

	     // Begin 06, 儲存到Log
	     checkBoxSaveLog = new Checkbox();
	     checkBoxSaveLog.setLabel(mLo.mStr[47][mLo.lan]);
	     checkBoxSaveLog.setSize(110,30);
	     mainFrame.add(checkBoxSaveLog);
	     checkBoxSaveLog.setState(Boolean.parseBoolean(mLo.FunPreferencesLoad("checkBoxSaveLog","false")));
	     checkBoxSaveLog.setLocation(10, y+120+tUITop);
	     checkBoxSaveLog.addItemListener(new ItemListener() {
	    	 	public void itemStateChanged(ItemEvent e) {             
	    	 		System.out.println(" Checkbox: " + (e.getStateChange()==1?"checked":"unchecked"));
	    	 		String tcheck="false";
	    	 		if (e.getStateChange()==1) { 		tcheck="true";   	 	}
	    	 		mLo.FunPreferencesSave("checkBoxSaveLog",tcheck);
	    	 	}
	     });
	     // END 06	
	 		 
	 // Begin 07, 選檔案按鈕
	 File f = new File(mLo.StringLogFileName);
	 //System.out.println(f.getName());
	 ButtonLogFileName = new Button(f.getName());   
	 ButtonLogFileName.setBounds(100,100, 140,30); 
	 mainFrame.add(ButtonLogFileName);
	 ButtonLogFileName.setLocation(120,y+120+tUITop); 
		 ButtonLogFileName.addActionListener(new ActionListener() {
		     public void actionPerformed(ActionEvent e) {
	  			 //ui_Setp1_listPorts();                                  // 找出LoRa USB COM ports 設備
				 // Begin 08, 選檔案
			 JFileChooser fileChooser = new JFileChooser();
			 fileChooser.setCurrentDirectory(new File(System.getProperty("user.home")));
			 //int result = fileChooser.showOpenDialog(this); //parent);  //Show up the dialog
			 int result = fileChooser.showSaveDialog(null);
			 if (result == JFileChooser.APPROVE_OPTION) {
				    // user selects a file
				    File selectedFile = fileChooser.getSelectedFile();
				    mLo.StringLogFileName=selectedFile.getAbsolutePath();     //储存Log 路径
				    mLo.FunPreferencesSave("StringLogFileName",mLo.StringLogFileName);
				    String LogFileName2=selectedFile.getName();
				    System.out.println("Selected file: " +mLo.StringLogFileName );
				    ButtonLogFileName.setLabel(LogFileName2);
			 }
			 // END 08, 選檔案
		    }
		  });
	  // END 07	   
		 
		 // Begin 06, 上傳到網路的選項 
	     checkBoxMQTT = new Checkbox();
	     checkBoxMQTT.setLabel(mLo.mStr[54][mLo.lan]);
	     checkBoxMQTT.setSize(150,30);
		 //mainFrame.add(checkBoxMQTT);
		 checkBoxMQTT.setState(Boolean.parseBoolean(mLo.FunPreferencesLoad("checkBoxMQTT","false")));
		 checkBoxMQTT.setLocation(10, y+150+tUITop);
		 checkBoxMQTT.addItemListener(new ItemListener() {
	    	 	public void itemStateChanged(ItemEvent e) {             
	    	 		System.out.println(" Checkbox: " + (e.getStateChange()==1?"checked":"unchecked"));
	    	 		String tcheck="false";
	    	 		if (e.getStateChange()==1) { 		tcheck="true";   	 	}
	    	 		mLo.FunPreferencesSave("checkBoxMQTT",tcheck);
	    	 	}
	     });
		 
		 
		 // END 06	
		 
	     // Begin 5,                 添加Step 1 一條區分線
		 Label lineLabel = new Label();
		 lineLabel.setAlignment(Label.LEFT);
		 lineLabel.setText("");     // "Select LoRa device"
		 lineLabel.setSize(H_SIZE,1);
		 lineLabel.setBackground(Color.lightGray );
		 mainFrame.add(lineLabel);  
		 lineLabel.setLocation(0, y+180+tUITop);
		 // END 5
		   
		   
		     
		 // Begin 2,  添加Step 3 「接收資料」的文字 
		 Label l4 = new Label();
		 l4.setAlignment(Label.LEFT);
		 l4.setText(mLo.mStr[58][mLo.lan]);     // "Select LoRa device"
		 l4.setSize(580,30);
		 mainFrame.add(l4);  
		 l4.setLocation(10, y+195+tUITop);
		 // END 2
	}
}