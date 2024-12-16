import argparse
from mido import MidiFile, MidiTrack, Message, MetaMessage

def encode_file_to_midi(input_file, output_midi, bps=120):
    """
    Encodes a binary file into a MIDI file.
    Each byte is represented as a MIDI note (0-127).
    
    Parameters:
        input_file (str): Path to the input binary file.
        output_midi (str): Path to the output MIDI file.
        bps (int): Beats per second for the MIDI tempo (default: 120).
    """
    if not output_midi:
        output_midi = input_file + ".mid"
    
    with open(input_file, "rb") as f:
        file_data = f.read()
    
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Set tempo based on BPS
    tempo = 60000000 // bps  # Microseconds per quarter note
    track.append(MetaMessage('set_tempo', tempo=tempo))

    print(f"Encoding file '{input_file}' to MIDI with tempo {bps} BPS...")
    for byte in file_data:
        note = byte % 128  # Map byte to a valid MIDI note range (0-127)
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=480))
    
    midi.save(output_midi)
    print(f"File encoded to MIDI and saved as '{output_midi}'")


def decode_midi_to_file(input_midi, output_file):
    if not output_file:
        output_file = input_midi.replace(".mid", ".bin")
    """
    Decodes a MIDI file back into the original binary file.
    
    Parameters:
        input_midi (str): Path to the input MIDI file.
        output_file (str): Path to the output binary file.
    """
    midi = MidiFile(input_midi)
    data = bytearray()
    
    print(f"Decoding MIDI file '{input_midi}' to binary...")
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                data.append(msg.note)
    
    with open(output_file, "wb") as f:
        f.write(data)
    
    print(f"MIDI decoded and saved as '{output_file}'")


def main():
    parser = argparse.ArgumentParser(description="Encode a binary file to MIDI and decode it back.")
    
    parser.add_argument(
        "-a",
        choices=["encode", "decode", "e", "d"],
        help="Action to perform: 'encode' or 'decode' (or shorthand: 'e' or 'd').",
    )
    parser.add_argument("-i", help="Path to the input file.")
    parser.add_argument("-o", help="Path to the output file.", default="",)
    parser.add_argument(
        "--bps", type=int, default=120, help="Beats per second for MIDI encoding (default: 120)."
    )
    
    args = parser.parse_args()
    
    # Map shorthand to full action names
    action = "encode" if args.a in ["encode", "e"] else "decode"
    
    if action == "encode":
        encode_file_to_midi(args.i, args.o, bps=args.bps)
    elif action == "decode":
        decode_midi_to_file(args.i, args.o)


if __name__ == "__main__":
    main()
