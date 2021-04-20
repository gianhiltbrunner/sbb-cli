## Transport info from switzerland on the CLI.
### Command line access to the http://transport.opendata.ch API.

	wget https://raw.githubusercontent.com/protelescristata/sbb-cli/master/sbb-cli.py
	chmod +x sbb-cli.py
* Requires python3

* usage: sbb-cli.py [-h] -f FROM -t TO [-c TIME] [-d DETAIL]

* optional arguments:
    *  -h, --help            show this help message and exit
    *  -f FROM, --from FROM  Departure station
    *  -t TO, --to TO        Arrival station
    *  -c TIME, --time TIME  Departure time
    *  -d DETAIL, --detail DETAIL Detailed information to connection [n]

#### Example Queries
* From station to Station: `sbb-cli.py -f Bern -t Olten -d 3`
* `sbb-cli.py -f Genf -t Landesmuseum`
* `sbb-cli.py -f Bern -t "Zürich, Bahnhofsstrasse 1" -c 14:39 -d 1`
Note: A lookup of the location is done first and the "best" location is chosen.  
So if we provide "Zürich" we will end up with "Zürich HB". To give a second 
example "Mosn" will become "Mosnang, Dorf".

    
#### Sample output:
            python3 sbb-cli.py -f "Apenzell" -t "Ramsei" -d 3
            [1] From: Appenzell (4A) At: 19:00 To: Ramsei At: 23:06 Duration: 4:06:00
            [2] From: Appenzell (3B) At: 19:30 To: Ramsei At: 23:29 Duration: 3:59:00
            [3] From: Appenzell (3B) At: 19:30 To: Ramsei At: 23:30 Duration: 4:00:00
            [4] From: Appenzell (4A) At: 20:00 To: Ramsei At: 23:29 Duration: 3:29:00
            [5] From: Appenzell (4A) At: 20:00 To: Ramsei At: 23:30 Duration: 3:30:00
            [6] From: Appenzell (4A) At: 20:00 To: Ramsei At: 00:06 Duration: 4:06:00
            [7] From: Appenzell (-) At: 21:05 To: Ramsei At: 00:29 Duration: 3:24:00
            [8] From: Appenzell (-) At: 21:05 To: Ramsei At: 00:30 Duration: 3:25:00
            [9] From: Appenzell (4B) At: 23:00 To: Ramsei, Bahnhof At: 03:21 Duration: 4:22:00

            Connection [3]:
            Station: Appenzell At: 19:30 Platform: (3B) "S 23 1192" Heading to: Gossau SG
            Station: Gossau SG At: 20:20 Platform: (4) "ICN 1538" Heading to: Lausanne
            Station: Olten At: 22:37 Platform: (9) "IR 2388" Heading to: Bern
            Station: Burgdorf At: 23:11 Platform: (4) "S 44 30085" Heading to: Hasle-Rüegsau
            Station: Hasle-Rüegsau At: 23:23 Platform: () "NFB 16585" Heading to: Sumiswald-Grünen
