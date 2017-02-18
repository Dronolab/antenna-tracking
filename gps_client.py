import gps

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        # print report
        if report['class'] == 'TPV':
            if hasattr(report, 'alt'):
                gpsBreakout_data = struct.pack("d", report.alt)
                print(report.alt)
            if hasattr(report, 'lon'):
                gpsBreakout_data += struct.pack("d", report.lon)
                print(report.lon)
            if hasattr(report, 'lat'):
                gpsBreakout_data += struct.pack("d", report.lat)
                print(report.lat)
            if hasattr(report, 'time'):
                print report.time
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print "GPSD has terminated"
