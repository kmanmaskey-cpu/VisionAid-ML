class Solution:
    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:
        N,M = len(mat[0]),len(mat)
        z = r*c
        if N*M != z:
            return mat
        else :
            list = []
            for i in mat:
                for z in i:
                    list.append(z)

            new_matrix = []
            for i in range(r):
                start_index = i * c
                end_index = start_index + c
                new_row = list[start_index : end_index]
                new_matrix.append(new_row)

            return new_matrix