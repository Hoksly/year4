def classify_lines(line1, line2, line3):
    A = line1
    B = line2
    C = line3

    def det(a, b):
        return a['A'] * b['B'] - a['B'] * b['A']

    def det3(a, b, c):
        return (a['A'] * (b['B'] * c['C'] - b['C'] * c['B'])
              - a['B'] * (b['A'] * c['C'] - b['C'] * c['A'])
              + a['C'] * (b['A'] * c['B'] - b['B'] * c['A']))

    def is_zero(x, eps=1e-9):
        return abs(x) < eps

    # Pairwise 2x2 determinants
    d_AB = det(A, B)
    d_AC = det(A, C)
    d_BC = det(B, C)

    mix_det = det3(A, B, C)

    def intersection(l1, l2):
        d = det(l1, l2)
        if is_zero(d):
            return None
        x = (l1['B'] * l2['C'] - l1['C'] * l2['B']) / d
        y = (l1['C'] * l2['A'] - l1['A'] * l2['C']) / d
        return (x, y)

    # Class 1: All lines coincide
    if is_zero(d_AB) and is_zero(line1['A']*line2['C'] - line2['A']*line1['C']) \
        and is_zero(line1['A']*line3['B'] - line3['A']*line1['B']) \
        and is_zero(line1['A']*line3['C'] - line3['A']*line1['C']):
        return 1, []

    # Class 2: All lines parallel (some could coincide)
    if is_zero(d_AB) and is_zero(d_AC) and \
       not is_zero((line1['A']*line2['C'] - line2['A']*line1['C'])**2 + \
                  (line1['A']*line3['C'] - line3['A']*line1['C'])**2):
        return 2, []

    # Class 3: All lines meet at one point
    if (not is_zero(d_AB) or not is_zero(d_AC) or not is_zero(d_BC)) and is_zero(mix_det):
        point = intersection(A, B)
        return 3, [point] if point else []

    # Class 4: Two intersections (two lines meet, one parallel or coincide)
    num_nonparallel = sum(not is_zero(d) for d in (d_AB, d_AC, d_BC))
    if num_nonparallel == 2:
        points = []
        if not is_zero(d_AB):
            points.append(intersection(A, B))
        if not is_zero(d_AC):
            points.append(intersection(A, C))
        if not is_zero(d_BC):
            points.append(intersection(B, C))
        return 4, points

    # Class 5: Three pairwise intersections (all lines different)
    if num_nonparallel == 3 and not is_zero(mix_det):
        points = [
            intersection(A, B),
            intersection(A, C),
            intersection(B, C)
        ]
        return 5, points

    return 0, []