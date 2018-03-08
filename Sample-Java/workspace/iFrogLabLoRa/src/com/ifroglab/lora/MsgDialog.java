package com.ifroglab.lora;

import java.awt.BorderLayout;
import java.awt.Button;
import java.awt.Dialog;
import java.awt.Event;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Panel;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

/*
public class MsgDialog {

}
*/

public  class MsgDialog extends Dialog {
	private static final long serialVersionUID = 1L;
	public MsgDialog(Frame parent,String iMsg,int iWidth,int iHight){
         super(parent, true);         
         //setBackground(Color.gray);
         mMsg=iMsg;
         mWidth=iWidth;
         mHight=iHight;
         setLayout(new BorderLayout());
         Panel panel = new Panel();
         panel.add(new Button("Close"));
         add("South", panel);
         setSize(iWidth,iHight);

         addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent windowEvent){
               dispose();
            }
         });
      }

      public boolean action(Event evt, Object arg){
         if(arg.equals("Close")){
            dispose();
            return true;
         }
         return false;
      }

      public void paint(Graphics g){
        // g.setColor(Color.white);
         g.drawString(mMsg, 20,mHight/2 );
      }
      private String mMsg;
      private int mWidth;
      private int mHight;
      
   }