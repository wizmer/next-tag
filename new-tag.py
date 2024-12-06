import subprocess
import re

def run_git():
    process = subprocess.run([
        'git', 'ls-remote', '--tags',
    ],                          stdout=subprocess.PIPE, universal_newlines=True)

    tags = [m.group(0) for line in process.stdout.split('\n')
            if (m := re.search('v[0-9]+\.[0-9]+(\.[0-9]+)?', line))]
    return tags

def find_latest(tags):
    versions = []
    for tag in tags:
        m = re.search('v([0-9]+)\.([0-9]+)(\.([0-9]+))?', tag)
        g = m.groups()
        versions.append([int(g[0]), int(g[1]), int(g[3] if g[3] is not None else 0)])
    latest = list(sorted(versions, reverse=True))[0]
    return latest

def next_tag():
    tags = run_git()
    latest = find_latest(tags)
    latest[-1] += 1
    return 'v{}.{}.{}'.format(latest[0],
                              latest[1],
                              latest[2])


def main():
    s = next_tag()
    print(f'Creating new tag: {s}')
    subprocess.run([
        'git', 'tag', '-a', s,
        '-m', f'Pushing tag {s}'
    ],
                             stdout=subprocess.PIPE, universal_newlines=True)
    subprocess.run([
        'git', 'push', 'origin', s
    ],
                             stdout=subprocess.PIPE, universal_newlines=True)


if __name__ =='__main__':
    main()
