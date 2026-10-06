from drumkit import *

def square_wave(frequency, amplitude, dur_time, sample_rate):

    dur_samples = round(dur_time * sample_rate)
    
    period_time = 1 / frequency
    period_samples = round(period_time * sample_rate)
    ps_half = round(period_samples / 2)

    repeat = round(dur_samples / period_samples)

    return fit(([-amplitude] * ps_half + [amplitude] * ps_half) * repeat, dur_samples)

def sawtooth_wave(frequency, amp, dur_time, sr = 48000):
    dur_samples = round(dur_time * sr)
    period_samples = round(sr / frequency)

    repeat = round(dur_samples / period_samples)
    return fit([amp * x / period_samples for x in range(period_samples)] * repeat, dur_samples)

def triangle_wave(frequency, amplitude, dur_time, sr = 48000):
    dur_samples = round(dur_time * sr)
    
    period_samples = round(sr / frequency)
    n_half = round(period_samples / 2)

    up = [-1 + 2 * x / n_half for x in range(n_half)]
    down = [1 - 2 * x / n_half for x in range(n_half)]

    # account for unlucky rounding
    if 2 * n_half < period_samples:
        down = down + [down[-1]]

    repeat = round(dur_samples / period_samples)
    
    tri_mult = (up + down) * repeat
    # apply amplitude
    triangle = vca(fit(tri_mult, dur_samples), [amplitude] * dur_samples)

    return triangle

def freq_from_semitones(base_frequency = 440, semitone = 0):
    return base_frequency * (2 ** (semitone / 12))

def render_bass(base_frequency, bass_sequence, steps_time, sample_rate = 48000):

    
    
    bass_waves_full = [
        mix(
            triangle_wave(
                freq_from_semitones(base_frequency, note), 
                0.2, 
                steps_time, 
                sample_rate
            ), 
            sawtooth_wave(
                freq_from_semitones(base_frequency, note),
                0.05,
                steps_time,
                sample_rate
            )
        ) for note in bass_sequence
    ]
    
    bass_waves_env = [
        vca(basswave, 
            envelope_exp(steps_time, tau = 0.2, sample_rate = sample_rate)
           ) for basswave in bass_waves_full
    ]
    
    bass_waves_fade = [
        edge_fade(basswave, attack = 0.001, release = 0.0005, sample_rate = sample_rate)
        for basswave in bass_waves_env
    ]
    
    return sum(bass_waves_fade, [])