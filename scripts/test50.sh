HOST=localhost:3000

SCORE=0

# Test [11]: Update Cell with Floating Point Number
ID="E1"; FORMULA="3.14"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [11]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [11]: FAIL (" $STATUS "!= 201 )"
fi

# Test [12]: Update Cell with Negative Number
ID="E2"; FORMULA="-5"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [12]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [12]: FAIL (" $STATUS "!= 201 )"
fi

# Test [13]: Update Cell with Complex Formula
ID="F1"; FORMULA="(3 + 4) * 2"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [13]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [13]: FAIL (" $STATUS "!= 201 )"
fi

# Test [14]: Read Cell with Negative Result
ID="E2" # Assuming E2 was set to a negative number in Test [12]
ANSWER="\"formula\":\"-5\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [14]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [14]: FAIL"
    fi
else
    echo "Test [14]: FAIL (" $STATUS "!= 200 )"
fi

# Test [15]: Delete Existing Cell
ID="F1" # Assuming F1 exists
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X DELETE -w "%{http_code}" $RESOURCE)
if [ $STATUS == "204" ]; then
    echo "Test [15]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [15]: FAIL (" $STATUS "!= 204 )"
fi

# Test [16]: List Cells After Deletion
RESOURCE=$HOST/cells
EXPECTED_LIST="[\"B2\",\"B3\",\"D4\",\"E1\",\"E2\"]" # Adjust based on expected cells after deletions

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    echo "Current List: $(cat body)"
    echo "Expected List: $EXPECTED_LIST"
    if [ "$(cat body)" == "$EXPECTED_LIST" ]; then
        echo "Test [17]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [17]: FAIL - List does not match expected"
    fi
else
    echo "Test [17]: FAIL (" $STATUS "!= 200 )"
fi

# Test [18]: Update Multiple Cells - Cell 1
ID1="G1"; FORMULA1="10"
RESOURCE1=$HOST/cells/$ID1

STATUS1=$(curl -s -X PUT -d "{\"id\":\"$ID1\",\"formula\":\"$FORMULA1\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE1)
if [ $STATUS1 == "201" ]; then
    echo "Test [18]: Cell 1 OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [18]: Cell 1 FAIL (" $STATUS1 "!= 201 )"
fi

# Test [17]: Update Multiple Cells - Cell 2
ID2="G2"; FORMULA2="20"
RESOURCE2=$HOST/cells/$ID2

STATUS2=$(curl -s -X PUT -d "{\"id\":\"$ID2\",\"formula\":\"$FORMULA2\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE2)
if [ $STATUS2 == "201" ]; then
    echo "Test [18]: Cell 2 OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [18]: Cell 2 FAIL (" $STATUS2 "!= 201 )"
fi


# Test [16]: Delete Non-Existent Cell
ID="Z9"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X DELETE -w "%{http_code}" $RESOURCE)
if [ $STATUS == "404" ]; then
    echo "Test [16]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [16]: FAIL (" $STATUS "!= 404 )"
fi


