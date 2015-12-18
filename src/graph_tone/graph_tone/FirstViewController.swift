//
//  FirstViewController.swift
//  graph_tone
//
//  Created by takanashi tomoyuki on 2015/10/07.
//  Copyright (c) 2015年 takanashi tomoyuki. All rights reserved.
//

import UIKit

class FirstViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Home"
        self.view.backgroundColor = UIColor.whiteColor()
        
        // Labelを作成.
        let myLabel: UILabel = UILabel(frame: CGRectMake(0,0,200,50))
        //myLabel.backgroundColor = UIColor.grayColor()
        myLabel.layer.cornerRadius = 20.0
        myLabel.text = "GraphTone!!"
        myLabel.font = UIFont.systemFontOfSize(CGFloat(30))
        // myLabel.textColor = UIColor.whiteColor()
        // myLabel.shadowColor = UIColor.grayColor()
        myLabel.textAlignment = NSTextAlignment.Center
        myLabel.layer.position = CGPoint(x: self.view.bounds.width/2,y:self.view.bounds.height*0.25)
        self.view.addSubview(myLabel)
        
        // ボタンを生成する.
        let inputButton: UIButton = UIButton(frame: CGRectMake(0,0,self.view.bounds.width*0.9,self.view.bounds.height*0.2))
        inputButton.backgroundColor = UIColor.blackColor()
        // inputButton.layer.masksToBounds = true
        inputButton.setTitle("数式入力", forState: .Normal)
        // inputButton.layer.cornerRadius = 20.0
        inputButton.titleLabel!.font = UIFont.systemFontOfSize(CGFloat(25))
        inputButton.layer.position = CGPoint(x: self.view.bounds.width/2 , y:self.view.bounds.height*0.63)
        inputButton.addTarget(self, action: "onClickInputButton:", forControlEvents: .TouchUpInside)
        
        let selectButton: UIButton = UIButton(frame: CGRectMake(0,0,self.view.bounds.width*0.9,self.view.bounds.height*0.2))
        selectButton.backgroundColor = UIColor.blackColor()
        // nextButton.layer.masksToBounds = true
        selectButton.setTitle("設定", forState: .Normal)
        selectButton.titleLabel!.font = UIFont.systemFontOfSize(CGFloat(25))
        // selectButton.layer.cornerRadius = 20.0
        selectButton.layer.position = CGPoint(x: self.view.bounds.width/2 , y:self.view.bounds.height*0.85)
        selectButton.addTarget(self, action: "onClickSelectButton:", forControlEvents: .TouchUpInside)
        
        // ボタンを追加する.
        self.view.addSubview(inputButton);
        self.view.addSubview(selectButton);
    }
    
    /* ボタンイベント */
    internal func onClickInputButton(sender: UIButton){
        // 画面遷移
        let inputViewController = InputViewController()
        self.navigationController?.pushViewController(inputViewController, animated: true)
    }
    
    internal func onClickSelectButton(sender: UIButton){
        
        // 画面遷移
        // let myViewController: UIViewController = SettingViewController()
        // self.navigationController?.pushViewController(myViewController, animated: true)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
