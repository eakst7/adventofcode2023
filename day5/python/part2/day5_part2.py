#!/usr/bin/env python3

input_data: str

class CompressedMap:

    def __init__(self):
        self.ranges: list[tuple[int,int,int]] = []
        self.filled = False
    
    def add_range(self, dest_range_start, src_range_start, range_len):
        self.ranges.append((dest_range_start, src_range_start, range_len))

    def get(self, v: int) -> int:
        for range in self.ranges:
            (dest_range_start, src_range_start, range_len) = range
            if (v >= src_range_start) and (v < (src_range_start+range_len)):
                return dest_range_start + (v - src_range_start)

        return v
    
    def fill_ranges(self) -> None:
        if self.filled:
            return

        self.filled = True
        ranges_to_add: list[tuple[int, int, int]] = []

        self.ranges = sorted(self.ranges, key=lambda t: t[1])

        index = 0
        for range in self.ranges:
            (dest_range_start, src_range_start, range_len) = range
            if index < src_range_start:
                ranges_to_add.append((index, index, src_range_start-index))
            index = src_range_start + range_len

        for r in ranges_to_add:
            self.ranges.append(r)
        self.ranges = sorted(self.ranges, key=lambda t: t[1])


    def get2(self, start, len) -> tuple[int,int]:
        self.fill_ranges()

        # # If this item is before the first defined range
        # first_range_start = self.ranges[0][1]
        # if start < first_range_start:
        #     return (start, min(len, first_range_start-start))
        
        last_range_end = self.ranges[-1][1] + self.ranges[-1][2] - 1
        if start > last_range_end:
            return (start, len)


        for range in self.ranges:
            (dest_range_start, src_range_start, range_len) = range
            src_range_end = src_range_start + range_len

            if (start >= src_range_start) and (start < src_range_end):
                return (dest_range_start + (start - src_range_start),min(len,src_range_end-start))

        return (start,len)
    
    def getall(self, src, srclen) -> list[tuple[int,int]]:
        l: list[tuple[int,int]] = []

        outlen = 0
        done = False
        while not done:
            (out,outlen) = self.get2(src,srclen)
            l.append((out,outlen))
            if (srclen == outlen):
                done = True
            else:
                src = src + outlen
                srclen = srclen - outlen

        return l

    def getall2(self, tuples: list[tuple[int,int]]) -> list[tuple[int,int]]:
        l: list[tuple[int,int]] = []

        for t in tuples:
            l = l + self.getall(t[0],t[1])

        return l


def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read()

def get_seeds() -> list[tuple[int,int]]:
    seeds_line = input_data.split("\n")[0]
    seeds = seeds_line.split(" ")[1:]

    seedlist = []
    for seedpair in seeds:
        (seedno,rangelen) = seedpair.split(",")
        seedlist.append((int(seedno), int(rangelen)))

    return seedlist

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
    lowest_location = None
    for seedpair in seeds:
        seed = seedpair[0]
        seedlen = seedpair[1]
        # print(f"{seed=}/{seedlen}")
        soil = seed_to_soil.getall2([(seed,seedlen)])
        fertilizer = soil_to_fertilizer.getall2(soil)
        water = fertilizer_to_water.getall2(fertilizer)
        light = water_to_light.getall2(water)
        temperature = light_to_temperature.getall2(light)
        humidity = temperature_to_humidity.getall2(temperature)
        location = humidity_to_location.getall2(humidity)

        for t in location:
            if lowest_location is None:
                lowest_location = t[0]
            else:
                lowest_location = min(lowest_location, t[0])

    print(f"{lowest_location=}")
    return lowest_location


if __name__ == "__main__":
    process("input2.txt")
