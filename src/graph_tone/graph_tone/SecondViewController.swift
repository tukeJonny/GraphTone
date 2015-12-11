//
//  SecondViewController.swift
//  graph_tone
//
//  Created by takanashi tomoyuki on 2015/10/07.
//  Copyright (c) 2015年 takanashi tomoyuki. All rights reserved.
//

import UIKit
import AVFoundation

class SecondViewController: UIViewController, UITextFieldDelegate, AVAudioPlayerDelegate, UIScrollViewDelegate {
    
    var myTextField: UITextField!
    var expLabel: UILabel!
    var rangeTextField1: UITextField!
    var rangeTextField2: UITextField!
    var myButton: UIButton!
    var backButton: UIButton!
    var myAudioPlayer : AVAudioPlayer!
    var myImageView: UIImageView!
    var myTextView: UITextView!
    var maxrange = 10
    var minrange = -10
    var count = 0
    let documentsPath = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0]
    let speech = AVSpeechSynthesizer()
    let myIP = "192.168.43.223"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "音声再生"
        self.navigationController?.navigationBar.frame.size.height = self.view.bounds.height*0.06
        self.view.backgroundColor = UIColor.whiteColor()
        
        let appDelegate: AppDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        let exp = appDelegate.expVal
        
        //TextFieldの生成.
        // myTextField = UITextField(frame: CGRectMake(0,0,self.view.bounds.width,60))
        // myTextField.text = "y=" + exp!
        // myTextField.delegate = self
        // myTextField.borderStyle = UITextBorderStyle.Line
        // myTextField.textAlignment = NSTextAlignment.Center
        // myTextField.layer.position = CGPoint(x:self.view.bounds.width/2, y:self.view.bounds.height*0.55);
        // self.view.addSubview(myTextField)
        
        expLabel = UILabel(frame: CGRectMake(0,0,self.view.bounds.width,60))
        expLabel.font = UIFont.systemFontOfSize(40)
        expLabel.text = "y=" + exp!
        expLabel.textAlignment = NSTextAlignment.Center
        expLabel.layer.position = CGPoint(x:self.view.bounds.width/2, y:self.view.bounds.height*0.55)
        self.view.addSubview(expLabel)
        
        rangeTextField1 = UITextField(frame: CGRectMake(0,0,100,50))
        rangeTextField1.text = String(maxrange)
        rangeTextField1.delegate = self
        rangeTextField1.borderStyle = UITextBorderStyle.Line
        rangeTextField1.textAlignment = NSTextAlignment.Center
        rangeTextField1.layer.position = CGPoint(x:self.view.bounds.width*0.8, y:self.view.bounds.height*0.68);
        self.view.addSubview(rangeTextField1)
        
        rangeTextField2 = UITextField(frame: CGRectMake(0,0,100,50))
        rangeTextField2.text = String(minrange)
        rangeTextField2.delegate = self
        rangeTextField2.borderStyle = UITextBorderStyle.Line
        rangeTextField2.textAlignment = NSTextAlignment.Center
        rangeTextField2.layer.position = CGPoint(x:self.view.bounds.width*0.2, y:self.view.bounds.height*0.68);
        self.view.addSubview(rangeTextField2)
        
        let label = UILabel(frame: CGRectMake(0, 0, 100, 50));
        label.text = " ≦ x ≦";
        label.layer.position = CGPoint(x:self.view.bounds.width*0.575, y:self.view.bounds.height*0.68);
        self.view.addSubview(label);
        
        // 画像表示
        let imagePath = "\(self.documentsPath)/output.png"
        self.myImageView = UIImageView(frame: CGRectMake(0,0,self.view.bounds.width*0.8, self.view.bounds.height*0.5))
        let myImage: UIImage = UIImage(contentsOfFile: imagePath)!
        self.myImageView.image = myImage
        self.myImageView.layer.position = CGPoint(x: self.view.bounds.width/2, y: self.view.bounds.height*0.26)
        self.view.addSubview(self.myImageView)
        
        // 音源設定
        // let soundFilePath : NSString = NSBundle.mainBundle().pathForResource("alarm1", ofType: "mp3")!
        // let fileURL : NSURL = NSURL(fileURLWithPath: soundFilePath as String)
        let soundPath = "\(self.documentsPath)/output.mp3"
        let fileURL : NSURL = NSURL(fileURLWithPath: soundPath)
        self.myAudioPlayer = try? AVAudioPlayer(contentsOfURL: fileURL)
        self.myAudioPlayer!.delegate = self
        
        //再生ボタンの生成.
        myButton = UIButton()
        myButton.frame.size = CGSizeMake(self.view.frame.width, 100)
        myButton.layer.position = CGPoint(x: self.view.frame.width/2, y:self.view.bounds.height*0.83)
        myButton.setTitle("音声再生", forState: UIControlState.Normal)
        myButton.titleLabel!.font = UIFont.systemFontOfSize(CGFloat(25))
        myButton.setTitleColor(UIColor.yellowColor(), forState: UIControlState.Normal)
        myButton.backgroundColor = UIColor.blackColor()
        myButton.addTarget(self, action: "onClickMyButton:", forControlEvents: UIControlEvents.TouchUpInside)
        self.view.addSubview(myButton)
        
        // backボタンを作成.
        backButton = UIButton(frame: CGRectMake(0,0,self.view.bounds.width,40))
        backButton.backgroundColor = UIColor.redColor();
        backButton.setTitle("戻る", forState: .Normal)
        backButton.layer.position = CGPoint(x:self.view.bounds.width/2 , y:self.view.bounds.height-25)
        // backButton.addTarget(self, action: "onClickbackButton:", forControlEvents: .TouchUpInside)
        self.view.addSubview(backButton);
    }
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        
        let spc = formulaCheck(myTextField.text!)
        print(spc)
        let utterance2 = AVSpeechUtterance(string: spc)
        utterance2.voice = AVSpeechSynthesisVoice(language: "ja-JP")
        utterance2.rate = 0.6
        speech.speakUtterance(utterance2)
        let utterance3 = AVSpeechUtterance(string: "下の再生ボタンを押してください")
        utterance3.voice = AVSpeechSynthesisVoice(language: "ja-JP")
        utterance3.rate = 0.6
        speech.speakUtterance(utterance3)
        
        return true
    }
    
    // ボタンがタップされた時に呼ばれるメソッド.
    func onClickMyButton(sender: UIButton){
        // exp = uriEncode(myTextField.text!)
        if myAudioPlayer.playing == true {
            //myAudioPlayerを一時停止.
            myAudioPlayer.pause()
            sender.setTitle("音声再生", forState: .Normal)
        } else {
            maxrange = Int(rangeTextField1.text!)!
            minrange = Int(rangeTextField2.text!)!
            let appDelegate: AppDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
            let host1 = appDelegate.hostUrl!
            let urlExp = uriEncode(appDelegate.expVal!)
            let host = "http://\(myIP):8080?expression=y=\(urlExp)&image=True&sound=True&range=\(minrange):\(maxrange)"
            
            if host1 != host {
                self.getData(host)
            } else {
                self.myAudioPlayer.play()
            }
            sender.setTitle("停止", forState: .Normal)
        }
        print("sender.currentTitile: \(sender.currentTitle)")
        print("sender.tag:\(sender.tag)")
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
                    
                    // 画像表示
                    let imagePath = "\(self.documentsPath)/output.png"
                    self.myImageView = UIImageView(frame: CGRectMake(0,0,260,260))
                    let myImage: UIImage = UIImage(contentsOfFile: imagePath)!
                    self.myImageView.image = myImage
                    self.myImageView.layer.position = CGPoint(x: self.view.bounds.width/2, y: self.view.bounds.height*0.26)
                    self.view.addSubview(self.myImageView)
                } else {
                    SVProgressHUD.showErrorWithStatus("失敗!")
                    // エラーハンドリング
                }
            }
        }
    }
    
    func audioPlayerDidFinishPlaying(player: AVAudioPlayer, successfully flag: Bool) {
        print("Music Finish")
        // 再度myButtonを"▶︎"に設定.
        myButton.setTitle("音声再生", forState: .Normal)
    }
    
    func audioPlayerDecodeErrorDidOccur(player: AVAudioPlayer, error: NSError?) {
        print("Error")
    }
    
    /* バックボタンイベント.
    internal func onClickbackButton(sender: UIButton){
        myAudioPlayer.pause()
        
        let myViewController: UIViewController = FirstViewController()
        //myViewController.modalTransitionStyle = UIModalTransitionStyle.FlipHorizontal
        self.presentViewController(myViewController, animated: true, completion: nil)
    }
    */
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // 読み上げ用の式変換
    func formulaCheck(str: String) -> String{
        var formula = str.stringByReplacingOccurrencesOfString("=", withString: "イコール")
        if formula.rangeOfString("^") != nil {
            formula = formula.stringByReplacingOccurrencesOfString("^", withString: "")
        }else{
            print("not hit")
        }
        print(formula)
        return formula
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
}
