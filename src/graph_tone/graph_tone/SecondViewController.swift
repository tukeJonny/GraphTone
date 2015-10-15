//
//  SecondViewController.swift
//  graph_tone
//
//  Created by takanashi tomoyuki on 2015/10/07.
//  Copyright (c) 2015年 takanashi tomoyuki. All rights reserved.
//

import UIKit
import AVFoundation

class SecondViewController: UIViewController, UITextFieldDelegate, AVAudioPlayerDelegate {
    
    var myTextField: UITextField!
    var outTextField: UITextField!
    var myButton: UIButton!
    var backButton: UIButton!
    var myAudioPlayer : AVAudioPlayer!
    var myImageView: UIImageView!
    var myLabel: UILabel!
    var myTextView: UITextView!
    var exp = ""
    let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as! String
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // 背景色を設定.
        self.view.backgroundColor = UIColor.whiteColor();
        
        //TextFieldの生成.
        myTextField = UITextField(frame: CGRectMake(0,0,200,30))
        myTextField.text = "HelloSwift!!"
        myTextField.delegate = self
        myTextField.borderStyle = UITextBorderStyle.RoundedRect
        myTextField.layer.position = CGPoint(x:self.view.bounds.width/2,y:500);
        self.view.addSubview(myTextField)
        
        //再生する音源のURLを生成.
        let soundFilePath : NSString = NSBundle.mainBundle().pathForResource("Juku", ofType: "mp3")!
        let fileURL : NSURL = NSURL(fileURLWithPath: soundFilePath as String)!
        myAudioPlayer = AVAudioPlayer(contentsOfURL: fileURL, error: nil)
        myAudioPlayer!.delegate = self
        
        //再生ボタンの生成.
        myButton = UIButton()
        myButton.frame.size = CGSizeMake(100, 100)
        myButton.layer.position = CGPoint(x: self.view.frame.width/2, y:400)
        myButton.setTitle("▶︎", forState: UIControlState.Normal)
        myButton.setTitleColor(UIColor.blackColor(), forState: .Normal)
        myButton.backgroundColor = UIColor.cyanColor()
        myButton.addTarget(self, action: "onClickMyButton:", forControlEvents: UIControlEvents.TouchUpInside)
        myButton.layer.masksToBounds = true
        myButton.layer.cornerRadius = 50.0
        self.view.addSubview(myButton)
        
        // ボタンを作成.
        backButton = UIButton(frame: CGRectMake(0,0,120,50))
        backButton.backgroundColor = UIColor.redColor();
        backButton.layer.masksToBounds = true
        backButton.setTitle("Back", forState: .Normal)
        backButton.layer.cornerRadius = 20.0
        backButton.layer.position = CGPoint(x: self.view.bounds.width/2 , y:self.view.bounds.height-50)
        backButton.addTarget(self, action: "onClickbackButton:", forControlEvents: .TouchUpInside)
        self.view.addSubview(backButton);
        
        myLabel = UILabel(frame: CGRectMake(0,0,200,50))
        myLabel.layer.cornerRadius = 20.0
        myLabel.text = ""
        myLabel.textAlignment = NSTextAlignment.Center
        myLabel.layer.position = CGPoint(x: self.view.bounds.width/2,y: 550)
        self.view.addSubview(myLabel)
        
    }
    
    // ボタンがタップされた時に呼ばれるメソッド.
    func onClickMyButton(sender: UIButton){
        if myAudioPlayer.playing == true {
            //myAudioPlayerを一時停止.
            myAudioPlayer.pause()
            sender.setTitle("▶︎", forState: .Normal)
        } else {
            
            exp = myTextField.text as String
            println(exp)
            // var myUrl:NSURL = NSURL(string:"http://localhost:8080")!
            let req1 = "http://localhost:8080?expression='"
            let req2 = "'&image=true&sound=true"
            let host = "http://localhost:8080?expression='"+exp+"'&image=true&sound=true"
            println(host)
            var myUrl:NSURL = NSURL(string:"http://localhost:8080?expression='"+exp+"'&image=true&sound=true")!
            var myRequest:NSURLRequest  = NSURLRequest(URL: myUrl)
            // NSURLConnection.sendAsynchronousRequest(myRequest, queue: NSOperationQueue.mainQueue(), completionHandler: self.getHttp)
            
            // 送信処理(同期)
            var res:NSData = NSURLConnection.sendSynchronousRequest(myRequest, returningResponse: nil, error: nil)!
            let fileData = res
            let fileName = "send.zip"
            let filePath = "\(documentsPath)/\(fileName)"
            fileData.writeToFile(filePath, atomically: true)
            
            println("-\(filePath)-")
            let fileManager = NSFileManager.defaultManager()
            var isDir : ObjCBool = false
            let isFile = fileManager.fileExistsAtPath(filePath, isDirectory: &isDir)
            if isFile{
                println("保存成功")
            }
            
            self.unZip(filePath) // 解凍
            
            // 画像表示
            let imagePath = "\(documentsPath)/send/image.png"
            myImageView = UIImageView(frame: CGRectMake(0,0,240,240))
            let myImage: UIImage = UIImage(contentsOfFile: imagePath)!
            myImageView.image = myImage
            myImageView.layer.position = CGPoint(x: self.view.bounds.width/2, y: 200.0)
            self.view.addSubview(myImageView)
            
            // 音源設定
            let soundPath = "\(documentsPath)/send/sound.mp3"
            let fileURL : NSURL = NSURL(fileURLWithPath: soundPath)!
            myAudioPlayer = AVAudioPlayer(contentsOfURL: fileURL, error: nil)
            myAudioPlayer!.delegate = self
            myAudioPlayer.play()
            
            myLabel.text = exp
            sender.setTitle("■", forState: .Normal)
        }
        
        println("sender.currentTitile: \(sender.currentTitle)")
        println("sender.tag:\(sender.tag)")
        
    }
    
    // 音楽再生が成功した時に呼ばれるメソッド.
    func audioPlayerDidFinishPlaying(player: AVAudioPlayer!, successfully flag: Bool) {
        println("Music Finish")
        
        // 再度myButtonを"▶︎"に設定.
        myButton.setTitle("▶︎", forState: .Normal)
    }
    
    // デコード中にエラーが起きた時に呼ばれるメソッド.
    func audioPlayerDecodeErrorDidOccur(player: AVAudioPlayer!, error: NSError!) {
        println("Error")
    }
    
    /* バックボタンイベント. */
    internal func onClickbackButton(sender: UIButton){
        
        myAudioPlayer.pause()
        
        // 遷移するViewを定義.
        let myViewController: UIViewController = FirstViewController()
        
        // アニメーションを設定.
        //myViewController.modalTransitionStyle = UIModalTransitionStyle.FlipHorizontal
        
        // Viewの移動.
        self.presentViewController(myViewController, animated: true, completion: nil)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func unZip(path: String){
        let zipPath = path //解凍するZIPファイルのパス
        let ret = SSZipArchive.unzipFileAtPath(zipPath, toDestination: documentsPath)
        if (ret) {
            // 処理が成功した場合
            println("解凍成功")
        }
    }
}
