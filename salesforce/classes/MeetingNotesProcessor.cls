public with sharing class MeetingNotesProcessor {
    public class Request {
        @InvocableVariable(required=true)
        public String transcript;
    }

    public class Response {
        @InvocableVariable
        public String normalizedTranscript;
    }

    @InvocableMethod(label='Normalize Synthetic Meeting Notes')
    public static List<Response> process(List<Request> requests) {
        List<Response> responses = new List<Response>();
        for (Request request : requests) {
            Response response = new Response();
            response.normalizedTranscript = String.isBlank(request.transcript)
                ? ''
                : request.transcript.trim();
            responses.add(response);
        }
        return responses;
    }
}

