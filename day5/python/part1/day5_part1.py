#!/usr/bin/env python3

input_data: str

class CompressedMap:

    def __init__(self):
        self.ranges: list[tuple[int,int,int]] = []
    
    def add_range(self, dest_range_start, src_range_start, range_len):
        self.ranges.append((dest_range_start, src_range_start, range_len))

    def get(self, v: int) -> int:
        for range in self.ranges:
            (dest_range_start, src_range_start, range_len) = range
            if (v >= src_range_start) and (v < (src_range_start+range_len)):
                return dest_range_start + (v - src_range_start)

        return v

def readinput(filename: str) -> str:
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def get_seeds() -> list[int]:
    seeds_line = input_data.split("\n")[0]
    seeds = seeds_line.split(" ")[1:]
    seeds = [int(seed) for seed in seeds]
    return seeds

def get_map_by_name(map: str) -> list[str]:
    for chunk in input_data.split("\n\n"):
        # print(f"{chunk=}")
        lines_in_chunk = chunk.split("\n")
        if lines_in_chunk[0].startswith(map):
            return lines_in_chunk[1:]

def process_map(map_input: list[str]) -> CompressedMap:
    output_map: CompressedMap = CompressedMap()
    for line in map_input:
        (dest_range_start, src_range_start, range_len) = line.split(" ")
        output_map.add_range(int(dest_range_start), int(src_range_start), int(range_len))

    return output_map


def process(filename: str) -> int:
    readinput(filename)

    seed_to_soil = process_map(get_map_by_name("seed-to-soil"))
    soil_to_fertilizer = process_map(get_map_by_name("soil-to-fertilizer"))
    fertilizer_to_water = process_map(get_map_by_name("fertilizer-to-water"))
    water_to_light = process_map(get_map_by_name("water-to-light"))
    light_to_temperature = process_map(get_map_by_name("light-to-temperature"))
    temperature_to_humidity = process_map(get_map_by_name("temperature-to-humidity"))
    humidity_to_location = process_map(get_map_by_name("humidity-to-location"))

    seeds = get_seeds()

    print(f"{seeds=}")
    locations: list[int] = []
    for seed in seeds:
        soil = seed_to_soil.get(seed)
        fertilizer = soil_to_fertilizer.get(soil)
        water = fertilizer_to_water.get(fertilizer)
        light = water_to_light.get(water)
        temperature = light_to_temperature.get(light)
        humidity = temperature_to_humidity.get(temperature)
        location = humidity_to_location.get(humidity)

        locations.append(location)

        # print(f"seed {seed} -> {fertilizer=} -> {water=} -> {light=} -> {temperature=} -> {humidity=} -> {location=}")

    location = min(locations)

    print(f"{location=}")
    return location


if __name__ == "__main__":
    process("input2.txt")
