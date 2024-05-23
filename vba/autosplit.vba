Sub SplitMergedCells()
    Dim ws As Worksheet
    Dim rng As Range
    Dim cell As Range
    Dim mergedCells As Range
    Dim i As Long
    'Works with Active Sheet!
    Set ws = ActiveSheet
    For Each cell In ws.UsedRange
        If cell.MergeCells Then
            Set mergedCells = cell.MergeArea
            mergedCells.MergeCells = False
            For i = 1 To mergedCells.Rows.Count
                mergedCells.Cells(i, 1).Value = cell.Value
            Next i
        End If
    Next cell

    MsgBox "All vertically merged cells have been split and their values copied top to bottom."
End Sub
