//
//  InputViewController.swift
//  graph_tone
//
//  Created by takanashi tomoyuki on 2015/11/20.
//  Copyright © 2015年 takanashi tomoyuki. All rights reserved.
//

import UIKit
import AVFoundation

class InputViewController: UIViewController, AVAudioPlayerDelegate {
    
    var resultLabel = UILabel()
    var resultTextView: UITextView!
    //一行に配置するボタンの数
    let xButtonCount = 5
    let yButtonCount = 6
    let screenWidth:Double = Double(UIScreen.mainScreen().bounds.size.width)
    let screenHeight:Double = Double(UIScreen.mainScreen().bounds.size.height)
    let buttonMargin = 0.0
    var exp = ""
    var expArray: [String] = []
    var expLabel = ""
    var expLabelArray: [String] = []
    var sendButton: UIButton!
    var count = 0
    let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0]
    let speech = AVSpeechSynthesizer()
    let appDelegate: AppDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
    var host1 = ""
    
    // IPアドレスの設定
    // let myIP = "192.168.43.223"         // nashiAP
    let myIP = "192.168.100.110"     // jony's wifi
    // let myIP = "192.168.1.3"         // my wifi
    
    let buttonLabels = [
        "sin","cos","tan","←","→",
        "x","x^2","x^3","□^x","log",
        "7","8","9","(",")",
        "4","5","6","+","-",
        "1","2","3","/","",
        "0","00",".","DEL","AC"
    ]
    
    let buttonVal = [
        "sin":"sin(", "cos":"cos(", "tan":"tan(", "←":"", "→":"",
        "x":"x", "x^2":"x^(2", "x^3":"x^(3", "□^x":"^(x", "log":"log(",
    ]
    
    let buttonTitles = [
        "サインかっこ","コサインかっこ","タンジェントかっこ","左に移動","右に移動",
        "x","x2乗","x3乗","x乗","ログかっこ",
        "7","8","9","かっこはじめ","かっこ終わり",
        "4","5","6","+","マイナス",
        "1","2","3","/","",
        "0","00","点","一つ戻る","すべて消す"
    ]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "数式入力"
        // NavigationBarにボタンを設置
        let settingButton: UIBarButtonItem!
        settingButton = UIBarButtonItem(title: "範囲", style: .Plain, target: self, action: "onClickSetButton:")
        self.navigationItem.rightBarButtonItem = settingButton
        self.view.backgroundColor = UIColor.whiteColor()
        
        sendButton = UIButton(frame: CGRectMake(0,0,self.view.bounds.width*0.98,self.view.bounds.height*0.12))
        sendButton.backgroundColor = UIColor.blackColor()
        sendButton.setTitle("音声生成", forState: .Normal)
        // sendButton.setTitleColor(UIColor.yellowColor(), forState: UIControlState.Normal)
        sendButton.titleLabel!.font = UIFont.systemFontOfSize(CGFloat(25))
        sendButton.layer.position = CGPoint(x:self.view.bounds.width/2 , y:self.view.bounds.height*0.93)
        sendButton.addTarget(self, action: "onClicksendButton:", forControlEvents: .TouchUpInside)
        self.view.addSubview(sendButton);
        
        let resultArea = self.view.bounds.height*0.2
        //式表示
        // resultLabel.textColor = UIColor.whiteColor()
        resultTextView = UITextView(frame: CGRectMake(self.view.bounds.width*0.03, self.view.bounds.height*0.11, self.view.bounds.width*0.94, resultArea))
        resultTextView.font = UIFont(name:"Arial", size: 40)
        resultTextView.textAlignment = NSTextAlignment.Right
        resultTextView.textColor = UIColor.whiteColor()
        // resultLabel.numberOfLines = 4
        resultTextView.text = "y="
        // resultLabel.textColor = UIColor.yellowColor()
        resultTextView.backgroundColor = UIColor.grayColor()
        resultTextView.editable = false
        self.view.addSubview(resultTextView)
        
        for var y=0; y<yButtonCount; y++ {
            for var x=0; x<xButtonCount; x++ {
                let button = UIButton()
                //let buttonHeight = (screenHeight - resultArea - ((buttonMargin*Double(yButtonCount)+1)))/Double(yButtonCount)
                let buttonPositionX = (screenWidth - 2.0) / Double(xButtonCount) * Double(x) + 2.0
                let tes = (screenHeight*0.95 - Double(resultArea) - buttonMargin - screenHeight*0.2) / Double(yButtonCount) * Double(y)
                let buttonPositionY = tes + buttonMargin + Double(resultArea*1.6)
                button.frame = CGRect(x:buttonPositionX, y:buttonPositionY, width:screenWidth*0.189, height:screenHeight*0.089)
                button.backgroundColor = UIColor.blackColor()
                
                let buttonNumber = y * xButtonCount + x
                button.tag = buttonNumber
                button.titleLabel!.font = UIFont.systemFontOfSize(CGFloat(25))
                button.setTitle(buttonLabels[buttonNumber],forState: UIControlState.Normal)
                // button.setTitleColor(UIColor.yellowColor(), forState: UIControlState.Normal)
                button.accessibilityLabel = buttonTitles[buttonNumber]
                print("num:\(buttonNumber), title:\(button.accessibilityLabel)")
                if buttonNumber == 3 || buttonNumber == 4 {
                    button.addTarget(self, action: "arrow_pushed:", forControlEvents: UIControlEvents.TouchUpInside)
                } else if buttonNumber == 24 {
                    
                } else {
                    button.addTarget(self, action: "button_pushed:", forControlEvents: UIControlEvents.TouchUpInside)
                }
                self.view.addSubview(button)
            }
        }
    }
    
    internal func onClicksendButton(sender: UIButton){
        if appDelegate.maxrange <= appDelegate.minrange  {
            print("range error")
            let utterance = AVSpeechUtterance(string: "選択範囲が不正です。設定しなおしてください")
            utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP")
            utterance.rate = 0.6
            let speech = AVSpeechSynthesizer()
            speech.speakUtterance(utterance)
            
        }else {
            if exp != "" {
                // 通信処理
                appDelegate.expVal = exp
                appDelegate.expLabelVal = expLabel
                let urlExp = uriEncode(exp)
                host1 = "http://\(myIP):8080?expression=y=\(urlExp)&image=True&sound=True&range=\(appDelegate.minrange):\(appDelegate.maxrange)"
                appDelegate.hostUrl = host1
                print(host1)
                self.getData(host1)
            } else {
                print("no exp")
                let utterance = AVSpeechUtterance(string: "式未入力です。式を入力してください。")
                utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP")
                utterance.rate = 0.6
                let speech = AVSpeechSynthesizer()
                speech.speakUtterance(utterance)
            }
            
        }
    }
    
    func button_pushed(sender:UIButton){
        let pushedNum:String = sender.titleLabel!.text!
        print("\(pushedNum)_pushed")
        switch pushedNum{
        case "DEL":
            if expArray.isEmpty{
                break
            } else {
                expArray.removeLast()
                expLabelArray.removeLast()
            }
        case "AC":
            exp = ""
            expArray = []
            expLabelArray = []
        default:
            if (buttonVal[pushedNum] != nil) {
                expArray.append(buttonVal[pushedNum]!)
            } else {
                expArray.append(pushedNum)
            }
            expLabelArray.append(buttonTitles[sender.tag])
            print(expLabelArray)
        }
        
        exp = ""
        for data in expArray {
            exp += data
        }
        print(exp)
        resultTextView.text = "y=" + exp
        
        expLabel = ""
        for labelData in expLabelArray {
            expLabel += labelData
        }
        print(expLabel)
        resultTextView.accessibilityLabel = "y=" + expLabel
        
    }
    
    internal func onClickSetButton(sender: UIButton){
        let myViewController: UIViewController = SettingViewController()
        self.navigationController?.pushViewController(myViewController, animated: true)
    }
    
    func arrow_pushed(sender:UIButton){
        
    }
    
    func getData(host: String){
        let myUrl:NSURL = NSURL(string: host)!
        let myRequest:NSURLRequest  = NSURLRequest(URL: myUrl)
        
        SVProgressHUD.showWithStatus("読み込み中")
        dispatch_async_global {
            // 送信処理(同期)
            
            let res:NSData = try! NSURLConnection.sendSynchronousRequest(myRequest, returningResponse: nil)
            let fileData = res
            let fileName = "send.zip"
            let filePath = "\(self.documentsPath)/\(fileName)"
            fileData.writeToFile(filePath, atomically: true)
            print("-\(filePath)-")
            
            // 解凍
            let ret = SSZipArchive.unzipFileAtPath(filePath, toDestination: self.documentsPath)
            if (ret) {
                // 処理が成功した場合
                print("解凍成功")
            }
            
            self.dispatch_async_main {
                let fileManager = NSFileManager.defaultManager()
                var isDir : ObjCBool = false
                let isFile = fileManager.fileExistsAtPath(filePath, isDirectory: &isDir)
                if isFile{
                    SVProgressHUD.showSuccessWithStatus("成功!")
                    print("保存成功")
                    let compVoice = AVSpeechUtterance(string: "音声の生成が完了しました")
                    compVoice.voice = AVSpeechSynthesisVoice(language: "ja-JP")
                    compVoice.rate = 0.6
                    self.speech.speakUtterance(compVoice)
                    
                    let myViewController: UIViewController = SecondViewController()
                    self.navigationController?.pushViewController(myViewController, animated: true)
                } else {
                    SVProgressHUD.showErrorWithStatus("失敗!")
                    // エラーハンドリング
                }
            }
        }
    }
    
    func uriEncode(str: String) -> String {
        return str.stringByAddingPercentEncodingWithAllowedCharacters(NSCharacterSet.alphanumericCharacterSet())!
    }
    
    func dispatch_async_main(block: () -> ()) {
        dispatch_async(dispatch_get_main_queue(), block)
    }
    
    func dispatch_async_global(block: () -> ()) {
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), block)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}