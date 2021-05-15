def findnum(num_list, num):
    end_row = len(num_list) - 1
    end_col = len(num_list[0]) - 1
    row = 0
    col = end_col
    while(row != end_row + 1 and col != -1):
        if( num < num_list[row][col]):
            col -= 1
        elif num > num_list[row][col]:
            row += 1
        else:
            return True
    return False



def findRepeatNumber(nums):
        num_list = [0 for x in range(len(nums))]
        for num in nums:
            num_list[num] += 1
        index = 0
        print(num_list)
        for num in num_list:
            if(num > 1):
                return num_list[index]
            index += 1

print(findRepeatNumber([2, 1, 1, 0, 4, 5, 3]))
