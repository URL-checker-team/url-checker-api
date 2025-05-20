def extract_features(url):
    return {
        'url_length': len(url),
        'has_https': int('https' in url),
        'num_dots': url.count('.'),
        'num_digits': sum(c.isdigit() for c in url),
        'num_special_chars': sum(not c.isalnum() for c in url),
        'count_www': url.count('www'),
        'count_at': url.count('@'),
        'count_slash': url.count('/'),
        'count_dash': url.count('-')
    }
