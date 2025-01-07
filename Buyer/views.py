from rest_framework.decorators import api_view
from rest_framework.response import Response
from link_market_backend.Buyer import models as buyerModels
from link_market_backend.Buyer import serializer as buyerSerailizer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def BuyersSignUp(request):
    if request.method == 'GET':
        try:
            buyers = buyerModels.BuyerSignUp.objects.all()
            serializer = buyerSerailizer.BuyerSignUpSerializer(buyers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': 'No data found', 'details': str(e)}, status=404)

    elif request.method == 'POST':
        serializer = buyerSerailizer.BuyerSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Buyer created successfully', 'data': serializer.data})
        return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)

    elif request.method == 'PUT':
        try:
            buyer_id = request.data.get('id')
            buyer = buyerModels.BuyerSignUp.objects.get(id=buyer_id)
            serializer = buyerSerailizer.BuyerSignUpSerializer(buyer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Buyer updated successfully', 'data': serializer.data})
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)
        except buyerModels.BuyerSignUp.DoesNotExist:
            return Response({'error': 'Buyer not found'}, status=404)
        except Exception as e:
            return Response({'error': 'An error occurred', 'details': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            buyer_id = request.GET.get('id')
            if not buyer_id:
                return Response({'error': 'ID parameter is required'}, status=400)
            buyerModels.BuyerSignUp.objects.filter(id=buyer_id).delete()
            return Response({'message': 'Buyer deleted successfully'})
        except Exception as e:
            return Response({'error': 'An error occurred', 'details': str(e)}, status=500)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def TasksData(request):
    if request.method == 'GET':
        tasks = buyerModels.BuyeTask.objects.filter(buyer_id=request.GET.get('buyer_id'))
        serializer = buyerSerailizer.TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = buyerSerailizer.TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task created successfully', 'data': serializer.data})
        return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)

    elif request.method == 'PUT':
        task_id = request.data.get('id')
        task = buyerModels.TaskCreation.objects.get(id=task_id)
        serializer = buyerSerailizer.TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task updated successfully', 'data': serializer.data})
        return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)

    elif request.method == 'DELETE':
        task_id = request.GET.get('id')
        buyerModels.TaskCreation.objects.filter(id=task_id).delete()
        return Response({'message': 'Task deleted successfully'})
