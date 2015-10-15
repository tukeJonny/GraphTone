//
//  ThirdViewController.swift
//  graph_tone
//
//  Created by takanashi tomoyuki on 2015/10/07.
//  Copyright (c) 2015年 takanashi tomoyuki. All rights reserved.
//

import UIKit

class ThirdViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.view.backgroundColor = UIColor.whiteColor();
        
        // Labelを作成.
        let myLabel: UILabel = UILabel(frame: CGRectMake(0,0,200,50))
        //myLabel.backgroundColor = UIColor.grayColor()
        myLabel.layer.cornerRadius = 20.0
        myLabel.text = "Hello Swift!!"
        myLabel.font = UIFont.systemFontOfSize(CGFloat(20))
        // myLabel.textColor = UIColor.whiteColor()
        // myLabel.shadowColor = UIColor.grayColor()
        myLabel.textAlignment = NSTextAlignment.Center
        myLabel.layer.position = CGPoint(x: self.view.bounds.width/2,y: 200)
        self.view.addSubview(myLabel)
        
        // ボタンを作成.
        let backButton: UIButton = UIButton(frame: CGRectMake(0,0,120,50))
        backButton.backgroundColor = UIColor.redColor();
        backButton.layer.masksToBounds = true
        backButton.setTitle("Back", forState: .Normal)
        backButton.layer.cornerRadius = 20.0
        backButton.layer.position = CGPoint(x: self.view.bounds.width/2 , y:self.view.bounds.height-50)
        backButton.addTarget(self, action: "onClickbackButton:", forControlEvents: .TouchUpInside)
        self.view.addSubview(backButton);
    }
    
    /* バックボタンイベント. */
    internal func onClickbackButton(sender: UIButton){
        
        let zipPath = "/Users/ne250114/Desktop/tdata.zip"  //解凍するZIPファイルのパス
        let destPath = "/Users/ne250114/Desktop/kaitou" //展開するディレクトリのパス
        let ret = SSZipArchive.unzipFileAtPath(zipPath, toDestination: destPath)
        if (ret) {
            // 処理が成功した場合
            println("解凍成功")
        }
        
        /* let destDirPath = "/Users/ne250114/Desktop"
        let zipFilesArr = [NSBundle.mainBundle().pathForResource("prab-xaxes2", ofType: "png"),
        NSBundle.mainBundle().pathForResource("Juku", ofType: "mp3")]
        let ret = SSZipArchive.createZipFileAtPath(destDirPath as String, withFilesAtPaths: zipFilesArr)
        if (ret) {
        // 処理が成功した場合
        println("Zip生成")
        } */
        
        // 遷移するViewを定義.
        let myViewController: UIViewController = FirstViewController()
        
        // アニメーションを設定.
        //myViewController.modalTransitionStyle = UIModalTransitionStyle.FlipHorizontal
        
        // Viewの移動.
        self.presentViewController(myViewController, animated: true, completion: nil)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    
}
