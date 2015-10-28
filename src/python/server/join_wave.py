import wave

def join_waves(inputs, output):
    '''
    inputs : list of filenames
    output : output filename
    '''
    try:
        fps = [wave.open(f, 'r') for f in inputs]
        fpw = wave.open(output, 'w')

        fpw.setnchannels(fps[0].getnchannels())
        fpw.setsampwidth(fps[0].getsampwidth())
        fpw.setframerate(fps[0].getframerate())
        
        for fp in fps:
            fpw.writeframes(fp.readframes(fp.getnframes()))
            fp.close()
        fpw.close()

    except wave.Error, e:
        print e

    except Exception, e:
        print 'unexpected error -> ' + str(e)

if __name__ == '__main__':
    inputs = ["./test.wav","./test2.wav"]
    output = 'sound.wav'

    join_waves(inputs, output)