import socket
import struct
import gps
import struct


#os.system("sudo killall gpsd")
#os.system("sudo gpsd /dev/tty/AMA0 -F /var/run/gpsd.sock")
gpssession = gps.gps("localhost", "2947")
gpssession.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

UDP_IP = "127.0.0.1"
UDP_PORT = 5008
s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
gpsBreakout_data = ""
while True :
    try:
        report = gpssession.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'alt'):
                gpsBreakout_data = struct.pack("d",report.alt)
            if hasattr(report, 'lon'):
                gpsBreakout_data += struct.pack("d",report.lon)
            if hasattr(report, 'lat'):
                gpsBreakout_data +=struct.pack("d",report.lat)
            if hasattr(report, 'time'):
                gpsBreakout_data +=struct.pack("d",report.time)
            s.sendto(gps_data,(UDP_IP,UDP_PORT))
    except KeyError:
		pass
    except KeyboardInterrupt:
		quit()
    except StopIteration:
		session = None
		print "GPSD has terminated"

       
