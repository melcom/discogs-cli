import discogs_client
import time

d = discogs_client.Client('discogscli/0.1',
                          user_token="cJYjyEDWioPNRKkoGamXuVJtdyaQGiMDWxWihkJX")

me = d.identity()
items = me.wantlist

wantlistmasters = []
wantlistmastersid = []
wantlistid = []

logs = open('logs.txt', 'r+')
alreadyprocessed = list(map(int, logs.read().splitlines()))

for item in iter(items):
    release = item.release
    wantlistid.append(release.id)
    if release.master.id not in wantlistmastersid:
        if release.master.id in alreadyprocessed:
            print("Already processed %d / %s" %
                  (release.master.id, release.title))
        else:
            wantlistmasters.append(release.master)
            wantlistmastersid.append(release.master.id)
            print("Release %d / %s" %
                  (release.master.id, release.title))

try:
    for master in wantlistmasters:
        print("=== main release %d / %s / %s / %s ===" %
              (master.main_release.id,
               master.main_release.title,
               master.main_release.country,
               master.main_release.year))
        for version in iter(master.versions):
            time.sleep(1)
            if version.country in ["US", "UK", "Germany", "Netherlands", "France", "Japan", "Europe", "UK & Europe"]:
                match = True
                for f in iter(version.formats):
                    if 'descriptions' in f and 'name' in f:
                        descriptions = f['descriptions']
                        name = f['name']
                        if "7\"" in descriptions:
                            match = False
                        if "RP" in descriptions:
                            match = False
                        if "RE" in descriptions:
                            match = False
                        if "RM" in descriptions:
                            match = False
                        if "Reissue" in descriptions:
                            match = False
                        if "Repress" in descriptions:
                            match = False
                        if "Remastered" in descriptions:
                            match = False
                        if name != "Vinyl":
                            match = False
                if match:
                    if version.id in wantlistid:
                        print("  !!! Already in wantlist     %d / %s / %s / %s " %
                              (version.id, version.title, version.country, version.year))
                    else:
                        print("  +++ Adding version          %d / %s / %s / %s" %
                              (version.id, version.title, version.country, version.year))
                        me.wantlist.add(version.id)
                else:
                    if version.id in wantlistid:
                        print("  --- Removing from wantlist  %d / %s / %s / %s " %
                              (version.id, version.title, version.country, version.year))
                        me.wantlist.remove(version.id)
                    else:
                        print("  *** No matching criteria    %d / %s / %s / %s " %
                              (version.id, version.title, version.country, version.year))
            else:
                print("  --- No matching country     %d / %s / %s / %s " %
                      (version.id, version.title, version.country, version.year))
        logs.write("%s" % master.id)
        logs.write("\n")
finally:
    logs.close()
