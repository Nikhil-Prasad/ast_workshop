"""
Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].

The test cases are generated so that the length of the output will never exceed 105.

Example 1:

Input: s = "3[a]2[bc]"
Output: "aaabcbc"
Example 2:

Input: s = "3[a2[c]]"
Output: "accaccacc"
Example 3:

Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
 

Constraints:

1 <= s.length <= 30
s consists of lowercase English letters, digits, and square brackets '[]'.
s is guaranteed to be a valid input.
All the integers in s are in the range [1, 300].

Solution Logic:

You are basically parsing a string again via a char/token concept. If the token is a digit, then you know that is the multipler. If the token is a [ then you know that you are opening up a loop to basically get the chars that must repeat until you see a ] (similar to the lexer concept of digit accumulation). Then you just iterate through the end of the list of s and end up with a new string. 

Because the brackets can be nested. We need a stack concept again. Similar to RPN. So the stack holds local memory. also i forgot about multiple digits.

I used a stack like RPN but this is basically just a pratt parser. Future attempt would do it fully recursively
"""


class Solution:

    def decodeString(self, s: str) -> str:
        stack = []
        current_str = ""
        current_num = 0

        for char in s:
            if char.isdigit():
                current_num = current_num * 10 + int(char)
            elif char == "[":
                stack.append((current_str, current_num))
                current_str = ""
                current_num = 0
            elif char == "]":
                prev_str, num = stack.pop()
                current_str = prev_str + (num * current_str)
            else:
                current_str += char

        return current_str

    
    #original attempt not understanding nested brackets
    def decodeStringOld(self, s: str) -> str:
        total = []
        for i, char in enumerate(s):
            if char.isdigit():
                multipler = int(char)
            if char == "[":
                char_list = []
                j = i + 1
                while j < len(s) and s[j] != "]":
                    char_list.append(s[j])
                digit_str = "".join(char_list)
                total.append(multipler * digit_str)
            else:
                total.append(char)
        
        return "".join(total)


if __name__ == "__main__":
    sol = Solution()
    
    # Test 1: Simple case
    test1 = "3[a]2[bc]"
    result1 = sol.decodeString(test1)
    expected1 = "aaabcbc"
    assert result1 == expected1, f"Test 1 failed: got {result1}, expected {expected1}"
    print(f"✅ Test 1: {test1} = {result1}")
    
    # Test 2: Nested brackets
    test2 = "3[a2[c]]"
    result2 = sol.decodeString(test2)
    expected2 = "accaccacc"
    assert result2 == expected2, f"Test 2 failed: got {result2}, expected {expected2}"
    print(f"✅ Test 2: {test2} = {result2}")
    
    # Test 3: Mixed with plain letters
    test3 = "2[abc]3[cd]ef"
    result3 = sol.decodeString(test3)
    expected3 = "abcabccdcdcdef"
    assert result3 == expected3, f"Test 3 failed: got {result3}, expected {expected3}"
    print(f"✅ Test 3: {test3} = {result3}")
    
    # Test 4: Multi-digit multiplier
    test4 = "10[a]"
    result4 = sol.decodeString(test4)
    expected4 = "aaaaaaaaaa"
    assert result4 == expected4, f"Test 4 failed: got {result4}, expected {expected4}"
    print(f"✅ Test 4: {test4} = {result4}")
    
    # Test 5: Deep nesting
    test5 = "2[2[y]pq4[2[jk]e1[f]]]ef"
    result5 = sol.decodeString(test5)
    expected5 = "yypqjkjkefjkjkefjkjkefjkjkefyypqjkjkefjkjkefjkjkefjkjkefef"
    assert result5 == expected5, f"Test 5 failed: got {result5}, expected {expected5}"
    print(f"✅ Test 5: {test5} = {result5}")
    
    print("\n✅ All tests passed!")
